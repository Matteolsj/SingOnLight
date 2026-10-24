"""Grove red LED output control, with a no-hardware simulation mode."""
from ..settings import SIMULATION_MODE

if SIMULATION_MODE:
    led = None
else:
    from grove.gpio import GPIO

    class GroveLed(GPIO):
        def __init__(self, pin):
            super().__init__(pin, GPIO.OUT)

        def on(self):
            """Turn the LED on."""
            self.write(1)

        def off(self):
            """Turn the LED off."""
            self.write(0)

    led = GroveLed(12)

def set_state(rhythm, index):
    """Set the LED state for a rhythm step and return the sequence."""
    if SIMULATION_MODE:
        return rhythm
    if rhythm[index] == 1:
        led.on()
    else:
        led.off()
    return rhythm
