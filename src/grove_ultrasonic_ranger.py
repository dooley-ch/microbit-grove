# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin8, sleep
from utime import sleep_us, ticks_us, ticks_diff

_HIGH     = 1
_LOW      = 0

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
        
        # Wait for previous pulse to end
        while self._pin.read_digital():
            if (ticks_diff(ticks_us(), begin) >= _TIME_OUT):
                return 0
            
        # Wait for pulse to start
        while not self._pin.read_digital():
            if (ticks_diff(ticks_us(), begin) >= _TIME_OUT):
                return 0
                
        pulse_begin = ticks_us()

        # Wait for pulse to stop
        while self._pin.read_digital():
            if (ticks_diff(begin, ticks_us()) >= _TIME_OUT):
                return 0
            
        pulse_end = ticks_us()
        
        pulse = ticks_diff(pulse_end, pulse_begin)
        # print("Pulse difference: {}".format(str(pulse)))
                
        return pulse
    
def demo():
    sensor = GroveUltrasonicRanger(pin8)
    
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
