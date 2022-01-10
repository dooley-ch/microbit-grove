# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# yellow, is tx and 16

from microbit import pin16, sleep, display, button_b

class GroveLineFinder:
    def __init__(self, pin):
        self._pin = pin
        
    def is_black(self):
        return not self._pin.read_digital()
    
def demo():
    sensor =  GroveLineFinder(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        if sensor.is_black():
            print('Black')
        else:
            print('White')
            
        sleep(500)

if __name__ == '__main__':




demo()
