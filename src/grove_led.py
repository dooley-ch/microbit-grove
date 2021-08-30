# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin0, sleep

class GroveLED:
    def __init__(self, pin):
        self._pin = pin
        
    def on(self):
        self._pin.write_digital(1)
    
    def off(self):
        self._pin.write_digital(0)

def demo():
    led = GroveLED(pin0)
    led.off()

    while True:
        led.on()
        sleep(1000)
        led.off()
        sleep(1000)
        
if __name__ == '__main__':
    demo()
