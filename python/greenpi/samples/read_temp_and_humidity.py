import os
import time

from hardware.DHT22 import DHT22

class TemperatureSample:
    def __init__(self, gpio_number):
        self.delay = 3
        self.gpio_number = gpio_number
    def run(self):
        try:
            dht = DHT22(self.gpio_number)
            while True:
                print("Humidity: %.2f" % (dht.get_humidity()) )
                print("Temperature: %.2f" % (dht.get_temperatur()) )
                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Cancel.")