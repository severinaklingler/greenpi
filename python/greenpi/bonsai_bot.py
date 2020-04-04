from gpiozero import OutputDevice
from signal import pause

relay1 = OutputDevice(pin=26,active_high=False)

relay1.on()

pause()