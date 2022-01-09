# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep, button_b, display

_HIGH           = 1
_LOW            = 0

class DigitalDistanceInterrupterSensor:
    def __init__(self, pin):
        self._pin = pin

    def is_triggered(self):
        return self._pin.read_digital() == _LOW
        
def main():
    sensor = DigitalDistanceInterrupterSensor(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if sensor.is_triggered():
            print('Is triggered!')
            
        sleep(500)

if __name__ == '__main__':
    main()
