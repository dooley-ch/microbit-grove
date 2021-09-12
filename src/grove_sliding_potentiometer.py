# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note:  This component requires an analog input, so the only valid pins are 0, 1, 2

from microbit import pin0, sleep, button_b, display

class GroveSlidingPotentiometer:
    def __init__(self, pin):
        self._pin = pin
        
    def value(self):
        return self._pin.read_analog()

def demo():
    meter = GroveSlidingPotentiometer(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        print("Reading: {}".format(str(meter.value())))
        sleep(2000)
        
if __name__ == '__main__':
    demo()