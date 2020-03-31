import spidev

# Interface to the MCP3008
#
# References
# See documentation/sensors/MCP3008.pdf for information about the sensor.

class MCP3008:
    START_BIT = 1
    DONT_CARE = 0 # byte ignored by the protocol
    SINGLE_ENDED = 8 # Communication type 

    def __init__(self, bus = 0, device = 0):
        self.bus = bus
        self.device = device
        self.default_clock_frequency = 1350000
        self.spi = spidev.SpiDev()
        self.open()
 
    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = self.default_clock_frequency
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([self.START_BIT, (self.SINGLE_ENDED | channel) << 4, self.DONT_CARE])

        # we get 10 bits in return (low to bits in first byte and full second byte)
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()