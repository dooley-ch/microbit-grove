# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# This sensor needs an analog in pin: P0, P1, P2

from microbit import pin0, sleep, button_b, display
from math import log

_B  = 4275   # B value of the thermistor
_R0 = 100000 # R0 = 100k

class GroveTemperatureSensor:
    def __init__(self, pin):
        self._pin = pin
        
    def get_temperature(self, fahrenheit = False):
        data = self._pin.read_analog()
        
        R = 1023.0 / data - 1.0
        R = _R0 * R
        
        value = 1.0 / (log(R / _R0) / _B + 1 / 298.15) - 273.15
        
        if fahrenheit:
            value = (value * 9/5) + 32

        return round(value)
    
def demo():
    sensor = GroveTemperatureSensor(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        print("Current Temperature: {0}C, {1}F".format(str(sensor.get_temperature()), str(sensor.get_temperature(True))))
        print()
        
        sleep(2000)
        
if __name__ == '__main__':
    demo()
