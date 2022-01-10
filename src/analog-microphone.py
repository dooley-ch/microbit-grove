# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note this component needs analog input, so P0, p1, p2

from microbit import pin0, sleep, button_b, display
from utime import sleep_ms

class AnalogMicrophone:
    def __init__(self, pin):
        self._pin = pin
        sleep_ms(50)
        
    def reading(self):
        return self._pin.read_analog()


def demo():
    sensor = AnalogMicrophone(pin0)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        print('Reading:', sensor.reading())
        sleep(500)
        
if __name__ == '__main__':
    demo()
