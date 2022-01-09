# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note: The relay lights up when turned on, so easy to check if working

from microbit import sleep, pin16, button_b, display

_HIGH = 1
_LOW = 0

class OptocouplerRelay:
    def __init__(self, pin):
        self._pin = pin
        self.off()
        
    def off(self):
        self._pin.write_digital(_LOW)
    
    def on(self):
        self._pin.write_digital(_HIGH)

def demo():
    relay = OptocouplerRelay(pin16)
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        print('Relay On')
        relay.on()
        sleep(6000)
        
        print('Relay Off')
        relay.off()
        sleep(6000)
        
if __name__ == '__main__':
    demo()
