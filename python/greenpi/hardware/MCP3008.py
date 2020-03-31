from spidev import SpiDev

# Interface to the MCP3008
#
# References
# See documentation/sensors/MCP3008.pdf for information about the sensor.

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus = bus
        self.device = device
        self.default_clock_frequency = 1350000
        self.spi = SpiDev()
        self.open()
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.set_max_speed_hz(self.default_clock_frequency)
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()