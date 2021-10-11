# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from micropython import const
from microbit import i2c, sleep
from utime import sleep_ms

_DEFAULT_ADDRESS         = const(0x38)

_AHTX0_CMD_INITIALIZE    = const(0xBE)
_AHTX0_CMD_TRIGGER       = const(0xAC)
_AHTX0_CMD_SOFTRESET     = const(0xBA)
_AHTX0_STATUS_BUSY       = const(0x80)
_AHTX0_STATUS_CALIBRATED = const(0x08)

class GroveDHT20Sensor:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        self._buffer = bytearray(6)

        self._reset()
        if not self._initialize():
            raise RuntimeError("Initialization failure")

    def _write_register(self, data):
        i2c.write(self._device_address, bytearray(data))
    
    def _read_register(self, num_bytes):
        # i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
    
    def _reset(self):
        self._write_register([_AHTX0_CMD_SOFTRESET])
        sleep_ms(20)
    
    def _initialize(self):
        self._write_register([_AHTX0_CMD_INITIALIZE, 0x08, 0x00])
        self._wait_for_idle()
        
        if not self._get_status() & _AHTX0_STATUS_CALIBRATED:
            return False
        
        return True
    
    def _wait_for_idle(self):
        while self._get_status() & _AHTX0_STATUS_BUSY:
            sleep_ms(5)
    
    def _read_data(self):
        self._write_register([_AHTX0_CMD_TRIGGER, 0x33, 0x00])
        self._wait_for_idle()
        self._buffer = self._read_register(6)
        
    def _get_status(self):
        self._buffer = self._read_register(6)
        # print("status: " + hex(self._buffer[0]))
        return self._buffer[0]
    
    def temperature(self, fahrenheit = False):
        self._read_data()
        
        temp = ((self._buffer[3] & 0xF) << 16) | (self._buffer[4] << 8) | self._buffer[5]
        temp = ((temp * 200.0) / 0x100000) - 50
        
        if fahrenheit:
            temp = (temp * 9/5) + 32

        return round(temp, 1)
    
    def relative_humidity(self):
        self._read_data()
        
        humidity = (self._buffer[1] << 12) | (self._buffer[2] << 4) | (self._buffer[3] >> 4)
        humidity = (humidity * 100) / 0x100000
        
        return round(humidity, 1)
    
def demo():
    sensor = GroveDHT20Sensor()
    
    temp = sensor.temperature()
    temp_fahrenheit = sensor.temperature(True)
    humi = sensor.relative_humidity()

    print("Temperature: {}C ({}F) Relative Humidity: {}%".format(str(temp), str(temp_fahrenheit), str(humi)))
    
if __name__ == '__main__':
    demo()
