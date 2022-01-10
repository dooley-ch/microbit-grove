# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, display, button_b, pin0

class GroveServoMotor:
    def __init__(self, pin):
        self._pin = pin
        self._pin.set_analog_period(20)
        self.move(0)
        
    def move(self, degrees):
        self._pin.write_analog(degrees)
        
def demo():
    motor = GroveServoMotor(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            motor.move(0)
            break
        
        motor.move(1)
        sleep(2000)
        
        motor.move(180)
        sleep(2000)
        
        motor.move(75)
        sleep(1000)
        motor.move(50)
        sleep(1000)
        motor.move(100)
        sleep(1000)

if __name__ == '__main__':
    demo()