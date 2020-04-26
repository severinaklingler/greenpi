import time
from signal import pause
import requests
from gpiozero import OutputDevice
from gpiozero import MCP3008
from hardware.DHT22 import DHT22
from hardware.hx711 import HX711

import numpy as np

import config as cfg

class Measurement:
    def __init__(self, sensor, value, tree_id):
        self.sensor = sensor
        self.value = value
        self.tree_id = tree_id

    def __str__(self):
        return '   ' + self.sensor + ' : ' + str(self.value)

class ServerConnection:
    def __init__(self, url, authorization_token):
        self.url = url
        self.authorization_token = authorization_token
        self.headers = {'Authorization': 'Token ' + self.authorization_token}

    def post(self, sub_path, data):
       return requests.post(self.url + sub_path, data=data, headers=self.headers)

class ConnectedSensorDevice:
    def __init__(self, server_connection):
        self.server_connection = server_connection
        self.measurements = []
    
    def update(self):
        self.measurements = []
        self.read_all_sensors()
        self.send_measurements()

    def read_all_sensors(self):
        pass

    def send_measurements(self):
        for m in self.measurements:
            data = {'value': m.value,'sensor': m.sensor,'tree_id': m.tree_id}
            self.server_connection.post('add_measurement/', data)

    def log_measurements(self):
        for m in self.measurements:
            print(m)


class BonsaiServant(ConnectedSensorDevice):
    def __init__(self, server_connection, tree_id, moisture_channel=0, water_channel=1, water_pump_gpio=26, sensor_switch_gpio=7, dht_gpio=17):
        super().__init__(server_connection)
        self.moisture = MCP3008(channel=moisture_channel)
        self.water_level = MCP3008(channel=water_channel)
        self.water_pump = OutputDevice(pin=water_pump_gpio,active_high=False)
        self.dht_sensor = DHT22(dht_gpio)
        self.current_moisture_level = 0
        self.sensor_switch = OutputDevice(pin=sensor_switch_gpio,active_high=True)
        self.server_connection = server_connection
        self.current_temperature = 0
        self.current_humidity = 0
        self.tree_id = tree_id
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("MSB", "MSB")
        referenceUnit = 261*1.34*0.9*1.05
        self.hx.set_reference_unit(referenceUnit)
        self.hx.set_offset(-5600)
        self.current_weight = 0

    def _enable_sensors(self):
        self.sensor_switch.on()
        time.sleep(0.300)

    def _disable_sensors(self):
        self.sensor_switch.off()

    def read_all_sensors(self):
        self._enable_sensors()
        self.current_moisture_level = self.moisture.value
        self.current_water_level = self.water_level.value
        self._disable_sensors()

        self.current_humidity = self.dht_sensor.get_humidity()
        self.current_temperature = self.dht_sensor.get_temperatur()
        self.read_weight()


        self.measurements.append(Measurement('moisture', self.current_moisture_level, self.tree_id))
        self.measurements.append(Measurement('water_tank_level', self.current_water_level, self.tree_id))
        self.measurements.append(Measurement('temperature', self.current_temperature, self.tree_id))
        self.measurements.append(Measurement('humidity', self.current_humidity, self.tree_id))
        self.measurements.append(Measurement('weigth', self.current_weight, self.tree_id))
        

    def _read_sensor(self, sensor):
        self._enable_sensors()
        value = sensor.value
        self._disable_sensors()
        return value

    def read_moisture(self):
        self.current_moisture_level = self._read_sensor(self.moisture.value)


    def read_weight(self):
        average_over_n = 10
        values = np.zeros(average_over_n)

        for i in range(average_over_n):
            values[i] = self.hx.get_weight(5)
            self.hx.power_down()
            self.hx.power_up()
            time.sleep(0.01)

        self.current_weight = np.mean(values)     

    def read_water_level(self):
        self.current_water_level = self._read_sensor(self.moisture.value)

    def water_tree(self, seconds=1):
        self.water_pump.on()
        time.sleep(seconds)
        self.water_pump.off()

    def update(self):
        super().update()

        if self.current_moisture_level < 0.5:
            # self.water_tree()
            print('water the tree')



try:
    server_connection = ServerConnection(cfg.url, cfg.authorization_token)
    servant = BonsaiServant(server_connection, cfg.tree_id, moisture_channel=0,water_channel=1,water_pump_gpio=26,sensor_switch_gpio=22,dht_gpio=17)
    
    while True:
        servant.update()
        servant.log_measurements()
        time.sleep(cfg.delay_seconds)

except KeyboardInterrupt:
    print("Cancel.")



# switch = OutputDevice(pin=22,active_high=True)
# print("on")
# switch.on()
# time.sleep(2)
# switch.off()
# time.sleep(2)

