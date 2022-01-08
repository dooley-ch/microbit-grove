# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note:  This component requires an analog input, so the only valid pins are 0, 1, 2

from microbit import pin0, sleep, button_b, display

class RotaryAngleSensor:
    _MAX_READING = 904
    
    def __init__(self, pin):
        self._pin = pin
        
    def value(self):
        return self._pin.read_analog()

    def percent(self):
        reading = self._pin.read_analog()
        return round(100 * (reading / RotaryAngleSensor._MAX_READING))

def main():
    sensor = RotaryAngleSensor(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        print("Reading: {} => {}%".format(sensor.value(), sensor.percent()))
        sleep(1000)
        
if __name__ == '__main__':
    main()