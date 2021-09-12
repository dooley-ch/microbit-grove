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

class GroveVibrationMotor:
    def __init__(self, pin):
        self._pin = pin
        
    def on(self):
        self._pin.write_digital(_HIGH)

    def off(self):
        self._pin.write_digital(_LOW)
        
def demo():
    motor = GroveVibrationMotor(pin16)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        motor.on()
        sleep(5000)
        motor.off()
        sleep(2000)
        
if __name__ == '__main__':
    demo()
