# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep, display, button_b

_HIGH           = 1
_LOW            = 0

class SwitchP:
    def __init__(self, pin):
        self._pin = pin
        
    def is_high(self):
        reading = self._pin.read_digital()        
        return (reading == _HIGH)
    
def main():
    button = SwitchP(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if button.is_high():
            print('Switch Is High')
        else:
            print('Switch Is Low')
            
        sleep(1000)

if __name__ == '__main__':
    main()
