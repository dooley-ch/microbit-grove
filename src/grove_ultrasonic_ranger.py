# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, sleep
from machine import time_pulse_us

from utime import sleep_us, ticks_us, ticks_diff

_HIGH     = 1
_LOW      = 0
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

_TIME_OUT = 1000000

class GroveUltrasonicRanger:
    def __init__(self, pin):
        self._pin = pin
        
    def measure_in_centimeters(self):
        duration = round(self._duration() / 29 / 2, 2)
        
        if duration < 0:
            return 0
        elif duration > 400:
            return 400
        else:
            return duration
        
    def measure_in_inches(self):
        duration = round(self._duration() / 74 / 2, 2)

        if duration < 0:
            return 0
        elif duration > 157:
            return 157
        else:
            return duration

    def _duration(self):
        self._pin.write_digital(_LOW)
        sleep_us(2)
        self._pin.write_digital(_HIGH)
        sleep_us(10)
        self._pin.write_digital(_LOW)
        
        begin = ticks_us()
                        
        return time_pulse_us(self._pin, 1)
    
def demo():
    sensor = GroveUltrasonicRanger(pin1)
    
    while True:
        range_in_inches = sensor.measure_in_inches()
        range_in_cm = sensor.measure_in_centimeters()
        
        print('The distance of obstacles in from is:')
        print('     ', range_in_inches, 'inches')
        print('     ', range_in_cm, 'centimeters')       
    
        sleep(2000)
        print('')

if __name__ == '__main__':
    demo()

