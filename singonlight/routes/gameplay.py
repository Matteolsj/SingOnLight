import sqlite3

from fastapi import HTTPException, Request

from ..devices import sound_sensor
from ..services import scoring
from ..services.game_service import (
    average_signal_by_interval,
    generate_rhythm,
    get_win_streak,
    increment_win_streak,
    record_score,
    reset_win_streak,
    save_game_settings,
)
from ..settings import DATABASE_PATH
from .pages import templates

story_level = 1


def parse_game_settings(body):
    try:
        interval_duration = float(body.get("interval_duration", 1))
        game_length = int(body.get("game_length", 25))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=422,
            detail="Interval duration and game length must be numbers.",
        )

    if not 0.1 <= interval_duration <= 2.0:
        raise HTTPException(
            status_code=422,
            detail="Interval duration must be between 0.1 and 2 seconds.",
        )
    if not 5 <= game_length <= 120:
        raise HTTPException(
            status_code=422,
            detail="Game length must be between 5 and 120 intervals.",
        )

    return interval_duration, game_length


def register_routes(app):
    @app.post("/api/play/multiplayer")
    async def play_multiplayer(request: Request):
        """Run one round for a player in the two-player mode."""
        body = await request.json()
        interval_duration, game_length = parse_game_settings(body)
        rhythm = body.get("rhythm", -1)
        if rhythm == -1:
            rhythm = generate_rhythm(game_length)
        elif (
            not isinstance(rhythm, list)
            or len(rhythm) != game_length
            or any(value not in (0, 1) for value in rhythm)
        ):
            raise HTTPException(status_code=422, detail="The submitted rhythm is invalid.")
        save_game_settings(interval_duration, game_length)

        readings = await sound_sensor.run_game(rhythm)
        observed_rhythm = average_signal_by_interval(readings, interval_duration)
        percentage = scoring.calculate_percentage(rhythm, observed_rhythm)
        record_score(percentage)
        return {
            "message": f"Finished with a score of {percentage}%.",
            "rhythm": rhythm,
            "percentage": percentage,
        }

    @app.post("/api/play")
    async def play_single_player(request: Request):
        """Run a single-player round using a random or custom rhythm."""
        body = await request.json()
        interval_duration, game_length = parse_game_settings(body)
        use_custom_rhythm = body.get("use_custom_rhythm", 0)

        if use_custom_rhythm not in (0, 1):
            raise HTTPException(status_code=422, detail="The custom-rhythm option is invalid.")

        if use_custom_rhythm == 1:
            with sqlite3.connect(DATABASE_PATH) as connection:
                rhythm = connection.execute(
                    "SELECT rhythm FROM rhythm WHERE id=1;"
                ).fetchone()[0]
            if rhythm in (None, "", "2"):
                raise HTTPException(
                    status_code=400,
                    detail="Save a custom rhythm before selecting this option.",
                )
            if (
                not 5 <= len(rhythm) <= 120
                or len(rhythm) != game_length
                or set(rhythm) - {"0", "1"}
            ):
                raise HTTPException(
                    status_code=400,
                    detail="The saved custom rhythm is invalid or does not match the selected game length.",
                )
            rhythm = [int(value) for value in rhythm]
        else:
            rhythm = generate_rhythm(game_length)

        save_game_settings(interval_duration, game_length)
        readings = await sound_sensor.run_game(rhythm)
        observed_rhythm = average_signal_by_interval(readings, interval_duration)
        percentage = scoring.calculate_percentage(rhythm, observed_rhythm)
        record_score(percentage)

        win_streak = get_win_streak()
        if percentage >= 50:
            if use_custom_rhythm == 0:
                win_streak = increment_win_streak()
            message = f"You won with a score of {percentage}%"
        else:
            if use_custom_rhythm == 0:
                win_streak = reset_win_streak()
            message = f"You lost with a score of {percentage}%"
        return {"message": message, "win_streak": win_streak}

    @app.get("/rhythm/create")
    def rhythm_creation_page(request: Request):
        """Show the custom rhythm editor with the saved rhythm, if any."""
        with sqlite3.connect(DATABASE_PATH) as connection:
            rhythm = connection.execute(
                "SELECT rhythm FROM rhythm WHERE id=1;"
            ).fetchone()[0]
            game_length = connection.execute(
                'SELECT value FROM settings WHERE key="game_length";'
            ).fetchone()[0]
        rhythm = "" if rhythm in (None, "", "2") else str(rhythm)
        return templates.TemplateResponse(
            request=request,
            name="rhythm_creation.html",
            context={"game_length": game_length, "rhythm": rhythm},
        )

    @app.post("/api/rhythm")
    async def save_custom_rhythm(request: Request):
        """Save a rhythm submitted by the custom rhythm editor."""
        body = await request.json()
        rhythm = body.get("rhythm", "")
        if (
            not isinstance(rhythm, str)
            or not 5 <= len(rhythm) <= 120
            or set(rhythm) - {"0", "1"}
        ):
            raise HTTPException(
                status_code=422,
                detail="Enter a rhythm between 5 and 120 beats long.",
            )
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                "UPDATE rhythm SET rhythm=? WHERE id=1;", (str(rhythm),)
            )
        return {"message": "Rhythm saved."}

    @app.post("/api/play/story")
    async def play_story_mode():
        """Play the current story level and return its result."""
        global story_level
        with sqlite3.connect(DATABASE_PATH) as connection:
            interval_duration, rhythm = connection.execute(
                "SELECT interval, rhythm FROM story WHERE key=?;", (story_level,)
            ).fetchone()
        rhythm = [int(value) for value in rhythm]
        readings = await sound_sensor.run_game(rhythm, interval_duration)
        observed_rhythm = average_signal_by_interval(readings, interval_duration)
        percentage = scoring.calculate_percentage(rhythm, observed_rhythm)
        record_score(percentage)

        win_threshold = 50 if story_level <= 5 else 60
        if story_level > 15:
            win_threshold = 70
        if percentage >= win_threshold:
            story_level += 1
            if story_level > 20:
                story_level = 1
                return {"message": "The story is complete!", "level": story_level, "state": "finished"}
            return {
                "message": f"You won with a score of {percentage}%",
                "level": story_level,
                "state": "won",
            }

        story_level = 1
        return {
            "message": f"You lost with a score of {percentage}%",
            "level": story_level,
            "state": "lost",
        }
