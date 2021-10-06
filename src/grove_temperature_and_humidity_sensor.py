# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from micropython import const
from microbit import pin0
from utime import sleep_ms, sleep_us, ticks_ms, ticks_us, ticks_diff

DHT_11       = const(11)
DHT_22       = const(22)

_CPU_SPEED   = const(6)
_MAX_TIMINGS = const(85)
_HIGH        = const(1)
_LOW         = const(0)
_NAN         = 999

class GroveTemperatureAndHumiditySensor:
    def __init__(self, pin, type):
        self._pin = pin
        self._data = bytearray([0, 0, 0, 0, 0])
        self._type = type
        self._last_read_time = 0
        self._first_reading = True
        
        self._pin.write_digital(_HIGH)
        
    def _read(self):
        last_state = _HIGH
        counter = 0
        current_time = None
        j = 0
    
        self._pin.write_digital(_HIGH)
        sleep_ms(250)
        
        current_time = ticks_ms()
        if current_time < self._last_read_time:
            self._last_read_time = 0
        
        if not self._first_reading and ticks_diff(current_time, self._last_read_time) < 2000:
            return True
        
        self._first_reading = False
        self._last_read_time = ticks_ms()
        
        print("self._data = {}".format(str(self._data)))
        
        self._data[0] = self._data[1] = self._data[2] = self._data[3] = self._data[4] = 0
        
        self._pin.write_digital(_LOW)
        sleep_ms(20)
        self._pin.write_digital(_HIGH)
        sleep_ms(40)
        
        for i in range(_MAX_TIMINGS):
            counter = 0
            
            while self._pin.read_digital() == last_state:
                counter += 1
                sleep_us(1)
                if counter == 255:
                    break
                
            last_state = self._pin.read_digital()
            if counter == 255:
                break
            
            if i >= 4 and i % 2 == 0:
                self._data[j / 8] <<= 1
                if counter > _CPU_SPEED:
                    self._data[j / 8] |= 1
                j += 1
        
        if j >= 40 and (self._data[4] == ((self._data[0] + self._data[1] + self._data[2] + self._data[3]) & 0xFF)):
            return True
        
        return False
    
    def get_temperature(self):
        if self._read():
            if self._type == DHT_11:
                value = float(self._data[2])
                return value
            
            if self._type == DHT_22:
                value = float(self._data[2] & 0x7F)
                value *= 256
                value += self._data[3]
                value /= 10
                
                if self._data[2] & 0x80:
                    value *= -1
                    
                return value
            
        return _NAN

    def get_temperature_faherheit(self):
        value = self.get_temperature()
    
    def get_humidity(self):
        if self._read():
            if self._type == DHT_11:
                return float(self._data[0])

            if self._type == DHT_22:
                value = float(self._data[0])
                value *= 256
                value += self._data[1]
                value /= 10

                return value
            
        return NAN
    
def demo():
    sensor = GroveTemperatureAndHumiditySensor(pin0, DHT_22)

    temp = sensor.get_temperature()
    hum = sensor.get_humidity()
    
    print("Current Temperature: {}, Humidity: {}".format(str(temp), str(hum)))
    
if __name__ == '__main__':
    demo()