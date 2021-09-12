# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin15, pin16, sleep, button_b, display

class GroveEncoder:
    def __init__(self, pin_a, pin_b):
        self._pin_a = pin_a
        self._pin_b = pin_b
        self._rotate_flag = None
        self._direction = None
        
        self._read()
        
    def _read(self):
        if self._pin_a.read_digital() > self._pin_b.read_digital():
            self._rotate_flag = 1
            self._direction = 1
            
        if self._pin_a.read_digital() < self._pin_b.read_digital():
            self._rotate_flag = 1
            self._direction = 0
            
    def get_rotate_flag(self):
        self._read()
        return self._rotate_flag
    
    def set_rotate_flag(self, value):
        self._rotate_flag = value
    
    def get_direction(self):
        self._read()
        return self._direction

def demo():
    encoder = GroveEncoder(pin15, pin16)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        if encoder.get_rotate_flag() == 1:
            if encoder.get_direction() == 0:
                print('Backward rotated')
            else:
                print('Forward rotated')
                
            encoder.set_rotate_flag(0)
            
        sleep(1000)
        
if __name__ == '__main__':
    demo()