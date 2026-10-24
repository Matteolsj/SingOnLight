import sqlite3
from random import randint
from ..settings import DATABASE_PATH

def reset_win_streak():
    """Reset the consecutive-win counter."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute('UPDATE settings SET value=0 WHERE key="win_streak";')
    return 0

def get_win_streak():
    """Return the current consecutive-win count."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            'SELECT value FROM settings WHERE key="win_streak";'
        ).fetchone()
    return row[0]

def increment_win_streak():
    """Increment and return the consecutive-win count."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        current_count = connection.execute(
            'SELECT value FROM settings WHERE key="win_streak";'
        ).fetchone()[0]
        new_count = current_count + 1
        connection.execute(
            'UPDATE settings SET value=? WHERE key="win_streak";',
            (new_count,),
        )
    return new_count

def average_signal_by_interval(signal, interval_duration):
    """Convert raw sound readings into one binary value per game interval."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        threshold = connection.execute(
            'SELECT value FROM settings WHERE key="threshold";'
        ).fetchone()[0]

    binary_signal = [1 if reading >= threshold else 0 for reading in signal]
    sample_period = 0.1
    samples_per_interval = round(interval_duration / sample_period)
    interval_averages = [
        sum(binary_signal[start:start + samples_per_interval]) / samples_per_interval
        for start in range(0, len(binary_signal), samples_per_interval)
    ]
    return [1 if average >= 0.5 else 0 for average in interval_averages]

def generate_rhythm(length):
    """Generate a random sequence of on/off beats."""
    return [randint(0, 1) for _ in range(length)]

def record_score(score_obtained):
    """Increment the database bucket containing the supplied score."""
    score_range = str(int((score_obtained // 10) * 10))
    with sqlite3.connect(DATABASE_PATH) as connection:
        current_count = connection.execute(
            'SELECT count FROM scores WHERE score_range=?;', (score_range,)
        ).fetchone()[0]
        connection.execute(
            'UPDATE scores SET count=? WHERE score_range=?;',
            (current_count + 1, score_range),
        )

def save_game_settings(interval_duration, game_length):
    """Persist the selected game settings for the next visit."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            'UPDATE settings SET value=? WHERE key="interval_duration";',
            (interval_duration,),
        )
        connection.execute(
            'UPDATE settings SET value=? WHERE key="game_length";',
            (game_length,),
        )

def save_calibration(threshold):
    """Save the selected or measured sound threshold."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            'UPDATE settings SET value=? WHERE key="threshold";', (threshold,)
        )