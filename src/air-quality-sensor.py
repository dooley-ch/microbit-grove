# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, sleep, display, button_b
from utime import ticks_ms, sleep_ms, ticks_diff

_FORCE_SIGNAL   = 0;
_HIGH_POLLUTION = 1;
_LOW_POLLUTION  = 2;
_FRESH_AIR      = 3;

class AirQualitySensor:
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
        if ticks_diff(ticks_ms(), self._last_std_vol_updated) > 500000:
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
        
def main():
    sensor = AirQualitySensor(pin1)
    
    display.clear()
    display.show('>')
              
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        slope = sensor.slope()
        
        if slope == _FRESH_AIR:
            print('Fresh Air')
        
        if slope == _HIGH_POLLUTION:
            print('Danger - High Pollution')
            
        if slope == _LOW_POLLUTION:
            print('Warning - Low Pollution')
        
        print('Air Quality Reading: ', sensor.get_quality())
        
        sleep(1000) 
        
if __name__ == '__main__':
    demo()

