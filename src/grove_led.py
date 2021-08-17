# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import *

class GroveLED:
    """
    This class supports the Grove LED.
    https://wiki.seeedstudio.com/Grove-LED_Socket_Kit
    """
    def __init__(self, pin):
        """
        Initializes an instance of the class with the pin that the LED has been connected
        """
        self._pin = pin
        
    def on(self)
        """
        Turns on the LED
        """
        self._pin.write_digital(1)
    
    def off(self):
        """
        Turns off the LED
        """
        self._pin.write_digital(0)
        
def main():
    """
    Demo for the class with the LED connected to pin 0
    """
    display.clear()

    led = GroveLED(pin0)
    led.off()

    while True:
        led.on()
        sleep(1000)
        led.off()
        sleep(1000)
    
if __name__ == '__main__':
    main()