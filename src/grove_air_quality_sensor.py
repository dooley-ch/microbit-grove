# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, pin8, pin16, sleep, set_volume
from utime import ticks_ms, sleep_ms, ticks_diff
import music

_FORCE_SIGNAL   = 0;
_HIGH_POLLUTION = 1;
_LOW_POLLUTION  = 2;
_FRESH_AIR      = 3;

class GroveLED:
    def __init__(self, pin):
        self._pin = pin
        
    def on(self):
        self._pin.write_digital(1)
    
    def off(self):
        self._pin.write_digital(0)

class GroveAirQualitySensor:
    def __init__(self, pin):
        self._pin = pin
        self._last_voltage = 0
        self._current_voltage = 0
        self._standard_voltage = 0
        self._voltage_sum = 0
        self._vol_sum_count = 0
        self._last_std_vol_updated = 0

        init_voltage = self._pin.read_analog()
        
        if (init_voltage > 10) and (init_voltage < 798):
            self._current_voltage = init_voltage;
            self._last_voltage = self._current_voltage;
            self._standard_voltage = init_voltage;
            self._last_std_vol_updated = ticks_ms();
        else:
            raise ValueError('Initial sensor reading out of range')
        
    def _updateStandardVoltage(self):
        if ticks_diff(ticks_ms(), self._last_std_vol_updated) < 500000:
            self._standard_voltage = self._voltage_sum / self._vol_sum_count;
            self._last_std_vol_updated = ticks_ms();

            self._voltage_sum = 0
            self._vol_sum_count = 0
    
    def slope(self):
        self._last_voltage = self._current_voltage
        self._current_voltage = self._pin.read_analog()

        self._voltage_sum = self._voltage_sum + self._current_voltage
        self._vol_sum_count = self._vol_sum_count + 1

        self._updateStandardVoltage()
        
        if ((self._current_voltage - self._last_voltage) > 400) or (self._current_voltage > 700):
            return _FORCE_SIGNAL
        elif ((self._current_voltage - self._last_voltage) > 400 and self._current_voltage < 700) or (self._current_voltage - self._standard_voltage) > 150:
            return _HIGH_POLLUTION
        elif (self._current_voltage - self._last_voltage) > 200 and self._current_voltage or (self._current_voltage - self._standard_voltage) > 50:
            return _LOW_POLLUTION
        else:
            return _FRESH_AIR

        return -1;
    
    def get_value(self):
        return self._current_voltage
    
    def get_quality(self):
        value = self.slope()
        
        if value == _FORCE_SIGNAL:
            return 'No Signal'
        elif value == _HIGH_POLLUTION:
            return 'High Pollution'
        elif value == _LOW_POLLUTION:
            return 'Low Polluiton!'
        else:
            return'Fresh Air'        
        
    
# For this demo, you need two LEDs one Red (P8) and one green (P16) as well as the air quality sensor (P1)
def demo():
    red_led = GroveLED(pin8)
    green_led = GroveLED(pin16)
    sensor = GroveAirQualitySensor(pin1)
  
    red_led.off()
    green_led.off()
            
    while True:
        slope = sensor.slope()
        
        if slope == _FRESH_AIR:
            green_led.on()
        
        if slope == _HIGH_POLLUTION:
            red_led.on()
            set_volume(255)
            music.play(music.FUNERAL)
            
        if slope == _LOW_POLLUTION:
            red_led.on()
        
        print('Air Quality:', sensor.get_quality())
        sleep(5000) 
        
if __name__ == '__main__':
    demo()

