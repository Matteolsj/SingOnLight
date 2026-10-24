"""Simulate ambient sound calibration without Raspberry Pi hardware."""
import asyncio
from singonlight.realtime.websocket_manager import broadcast

async def simulate_calibration(duration_seconds):
    """
    Return the simulated ambient sound threshold.
    """
    sampling_interval = 0.1

    await broadcast("Please remain quiet while ambient sound is calibrated.")
    print("Please remain quiet while ambient sound is calibrated.")
    await asyncio.sleep(5)
    for seconds_remaining in range(3, 0, -1):
        await broadcast("Calibration starts in " + str(seconds_remaining) + " seconds")
        print("Calibration starts in", seconds_remaining, "seconds")
        await asyncio.sleep(1)
    await broadcast("Ambient sound calibration in progress. Please remain quiet.")
    print("Silence")
    readings = []
    for _ in range(int(duration_seconds * (1 / sampling_interval))):
        readings.append(0)
        await asyncio.sleep(sampling_interval)
    threshold = (sum(reading**2 for reading in readings) / len(readings)) ** 0.5
    await broadcast("Ambient sound calibration complete. (" + str(threshold) + ")")
    print("Ambient sound calibration complete")
    return threshold