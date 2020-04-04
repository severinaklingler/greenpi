import time
from signal import pause

from gpiozero import OutputDevice
from gpiozero import MCP3008



moisture = MCP3008(channel=0)
water_level = MCP3008(channel=1)
relay1 = OutputDevice(pin=26,active_high=False)
delay = 1

relay1.on()
time.sleep(10)
relay1.off()


try:
    while True:
        print('Moisture ' + str(moisture.value))
        print('Water level ' + str(water_level.value))
        
        if moisture.value > 0.05:
            relay1.on()
            time.sleep(1)
            relay1.off()

        time.sleep(delay)

except KeyboardInterrupt:
    print("Cancel.")
