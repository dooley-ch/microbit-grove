# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# This sensor requires analog input, so use P0, P1, P2

from microbit import pin0, sleep, display, button_b

class GroveLoudnessSensor:
    def __init__(self, pin):
        self._pin = pin
            
    def reading(self):
        return self._pin.read_analog()
    
def demo():
    sensor = GroveLoudnessSensor(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break;
        
        print('Sound Reading:', sensor.reading())
        sleep(200)

if __name__ == '__main__':
    demo()
