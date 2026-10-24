import sqlite3
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

from ..settings import DATABASE_PATH

PACKAGE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))


def get_chart_data():
    with sqlite3.connect(DATABASE_PATH) as connection:
        scores = connection.execute("SELECT score_range, count FROM scores;").fetchall()

    chart_data = []
    for score_range, count in scores:
        label = "100%" if score_range == "100" else f"{score_range}-{int(score_range) + 9}%"
        chart_data.append([label, count])
    return chart_data


def register_routes(app):
    @app.get("/")
    def home(request: Request):
        return templates.TemplateResponse(request=request, name="index.html")

    @app.get("/modes")
    def modes(request: Request):
        return templates.TemplateResponse(request=request, name="modes.html")

    @app.get("/story")
    def story(request: Request):
        return templates.TemplateResponse(request=request, name="story.html")

    @app.get("/play/multiplayer")
    def multiplayer_page(request: Request):
        with sqlite3.connect(DATABASE_PATH) as connection:
            interval_duration = connection.execute(
                'SELECT value FROM settings WHERE key="interval_duration";'
            ).fetchone()[0]
            game_length = connection.execute(
                'SELECT value FROM settings WHERE key="game_length";'
            ).fetchone()[0]
        return templates.TemplateResponse(
            request=request,
            name="play_multiplayer.html",
            context={
                "interval_duration": interval_duration,
                "game_length": game_length,
            },
        )

    @app.get("/play")
    def play_page(request: Request):
        with sqlite3.connect(DATABASE_PATH) as connection:
            interval_duration = connection.execute(
                'SELECT value FROM settings WHERE key="interval_duration";'
            ).fetchone()[0]
            game_length = connection.execute(
                'SELECT value FROM settings WHERE key="game_length";'
            ).fetchone()[0]
            win_streak = connection.execute(
                'SELECT value FROM settings WHERE key="win_streak";'
            ).fetchone()[0]
            rhythm = connection.execute(
                "SELECT rhythm FROM rhythm WHERE id=1;"
            ).fetchone()[0]
        has_custom_rhythm = rhythm not in (None, "", "2", -1)
        rhythm_length = len(str(rhythm)) if has_custom_rhythm else 0
        return templates.TemplateResponse(
            request=request,
            name="play.html",
            context={
                "interval_duration": interval_duration,
                "game_length": game_length,
                "win_streak": win_streak,
                "rhythm": rhythm_length,
                "has_custom_rhythm": has_custom_rhythm,
            },
        )

    @app.get("/play/story")
    def story_game_page(request: Request):
        with sqlite3.connect(DATABASE_PATH) as connection:
            rhythm = connection.execute(
                "SELECT rhythm FROM story WHERE key=1;"
            ).fetchone()[0]
        return templates.TemplateResponse(
            request=request,
            name="play_story.html",
            context={"rhythm": rhythm},
        )

    @app.get("/data")
    def data_page(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="data.html",
        )

    @app.get("/api/data/scores")
    def get_scores():
        return get_chart_data()

    @app.get("/calibration")
    def calibration_page(request: Request):
        with sqlite3.connect(DATABASE_PATH) as connection:
            threshold = connection.execute(
                'SELECT value FROM settings WHERE key="threshold";'
            ).fetchone()[0]
        return templates.TemplateResponse(
            request=request,
            name="calibration.html",
            context={"threshold": int(threshold)},
        )

    @app.post("/api/data/reset")
    async def reset_data(request: Request):
        """Clear all recorded score counts."""
        with sqlite3.connect(DATABASE_PATH) as connection:
            for score_range in range(0, 101, 10):
                connection.execute(
                    "UPDATE scores SET count=0 WHERE score_range=?;",
                    (str(score_range),),
                )
        return {"status": "Game data has been reset."}
