# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note: When the relay is active the red light will be on, so no need to hook up a device to
# test it.

from microbit import sleep, pin16, button_b, display

_HIGH = 1
_LOW = 0

class Relay:
    def __init__(self, pin):
        self._pin = pin
        self.off()
        
    def off(self):
        self._pin.write_digital(_LOW)
    
    def on(self):
        self._pin.write_digital(_HIGH)

def main():
    component = Relay(pin16)
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        print('Relay On')
        component.on()
        sleep(2000)
        
        print('Relay Off')
        component.off()
        sleep(2000)
        
if __name__ == '__main__':
    main()

