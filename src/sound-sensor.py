# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# This sensor requires analog input, so use P0, P1, P2

from microbit import pin0, sleep, display, button_b

class SoundSensor:
    def __init__(self, pin):
        self._pin = pin
            
    def reading(self):
        value = 0
        
        for i in range(32):
            value += self._pin.read_analog()
            
        return (value >> 5)
    
def main():
    sensor = SoundSensor(pin0)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break;
        
        print('Sound Reading:', sensor.reading())
        sleep(500)

if __name__ == '__main__':
    main()
