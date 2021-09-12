# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

_HIGH = 1
_LOW  = 0

from microbit import pin16, sleep, button_b, display

class GrovePassivePuzzer:
    def __init__(self, pin):
        self._pin = pin
        
    def on(self):
        self._pin.write_digital(_HIGH)

    def off(self):
        self._pin.write_digital(_LOW)
        
def demo():
    buzzer = GrovePassivePuzzer(pin16)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        buzzer.on()
        sleep(1000)
        buzzer.off()
        sleep(1000)
        
if __name__ == '__main__':
    demo()
