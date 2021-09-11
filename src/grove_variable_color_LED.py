# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# NOTE:
# Despite being rated for a 5v power source, it does work with the Micro:bit even when the
# breakout board is not powered by a 5v connection!
#
# The RGB colors can be changed using a screwdriver on the board, if you have the time and
# patience to do it.
#
# The fading is not great, but on and off work OK.

from microbit import pin16, sleep, display, button_a, button_b
from utime import sleep_ms

class GroveVariableColorLED:
    def __init__(self, pin):
        self._pin = pin
        self.off()
        
    def off(self):
        self._pin.write_digital(1)
        sleep_ms(50)
    
    def on(self):
        self._pin.write_digital(0)
        sleep_ms(50)
                
    def fade(self, value):
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
            
        self._pin.write_analog(value)

def demo():
    led = GroveVariableColorLED(pin16)
    display.show('<')
    
    while True:
        if button_b.is_pressed():
            break
        
        if button_a.is_pressed():
            for i in range(10):
                led.on()
                sleep(500)
                led.off()
                sleep(500)
            led.off()
            
        sleep(1000)
        
if __name__ == "__main__":
    demo()
