# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Analog input so use pins: P0, P1, P2

from microbit import sleep, pin1, pin2, display, button_b

class GroveThumbJoystick:
    def __init__(self, pin_x, pin_y):
        self._pin_x = pin_x
        self._pin_y = pin_y
        
    def value(self):
        data_x = self._pin_x.read_analog()
        data_y = self._pin_y.read_analog()
        
        return data_x, data_y
    
def demo():
    js = GroveThumbJoystick(pin1, pin2)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        x, y = js.value()
        print("X, Y = {0}, {1}".format(x, y))
        
        if x > 900:
            print('Joystick Pressed')
            
        sleep(0.2)
    

if __name__ == '__main__':
    demo()
