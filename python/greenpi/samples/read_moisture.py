import os
import time

from hardware import MCP3008

class MoistureSample:
    def __init__(self):
        self.delay = 0.2
    def run(self):
        try:
        adc = MCP3008()
        while True:
            value = adc.read( channel = 0 )
            print("Voltage: %.2f" % (value / 1024.0 * 3.3) )
            time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Cancel.")