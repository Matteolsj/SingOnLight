"""Grove sound sensor input and calibration routines."""
import asyncio
import sqlite3
from ..realtime.websocket_manager import broadcast
from ..settings import DATABASE_PATH, SIMULATION_MODE
from . import led

if not SIMULATION_MODE:
    from grove.adc import ADC

    class GroveSoundSensor:
        def __init__(self, channel):
            self.channel = channel
            self.adc = ADC()

        @property
        def sound(self):
            return self.adc.read(self.channel)

async def run_game(rhythm, story_interval_duration=None):
    """Play a light sequence while collecting sound-sensor readings."""
    sample_period = 0.1

    if story_interval_duration is None:
        with sqlite3.connect(DATABASE_PATH) as connection:
            interval_duration = connection.execute(
                'SELECT value FROM settings WHERE key="interval_duration";'
            ).fetchone()[0]
    else:
        interval_duration = story_interval_duration

    if SIMULATION_MODE:
        samples_per_interval = round(interval_duration / sample_period)
        return [
            100 if beat else 0
            for beat in rhythm
            for _ in range(samples_per_interval)
        ]

    sensor = GroveSoundSensor(channel=0)

    readings = []
    for step, _ in enumerate(rhythm):
        led.set_state(rhythm, step)
        for _ in range(round(interval_duration / sample_period)):
            readings.append(sensor.sound)
            await asyncio.sleep(sample_period)

    led.set_state([0], 0)
    return readings

async def calibration(duration_seconds):
    """Measure ambient sound and return its root-mean-square level."""
    if SIMULATION_MODE:
        await broadcast("Simulated calibration complete. (50)")
        return 50

    sensor = GroveSoundSensor(channel=0)
    sample_period = 0.1

    await broadcast("Please remain quiet during ambient sound calibration.")
    await asyncio.sleep(5)
    for seconds_left in range(3, 0, -1):
        await broadcast(f"Calibration starts in {seconds_left} seconds.")
        await asyncio.sleep(1)

    await broadcast("Calibration is in progress. Please stay quiet.")
    readings = []
    for _ in range(int(duration_seconds / sample_period)):
        readings.append(sensor.sound)
        await asyncio.sleep(sample_period)

    threshold = (sum(value ** 2 for value in readings) / len(readings)) ** 0.5
    await broadcast(f"Ambient sound calibration complete. ({threshold})")
    return threshold
