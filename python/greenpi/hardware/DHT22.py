import time

import Adafruit_DHT

class DHT22:
    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.sensor = Adafruit_DHT.DHT22
        self.humidity = 0
        self.temperature = 0
        self.last_read_sensor = 0

    def _is_new_data_available(self):
        current_time = time.time()
        return current_time - self.last_read_sensor >= 2

    def _read_sensor(self):
        if self._is_new_data_available():
            self.humidity, self.temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio_number)
            self.last_read_sensor = time.time()

    def get_temperatur(self):
        self._read_sensor()
        return self.temperature

    def get_humidity(self):
        self._read_sensor()
        return self.humidity