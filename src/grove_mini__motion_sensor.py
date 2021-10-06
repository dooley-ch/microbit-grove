# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep, display, button_b

class GroveMiniPIRSensorSensor:
    def __init__(self, pin):
        self._pin = pin
            
    def reading(self):
        return self._pin.read_digital()
    
def demo():
    sensor = GroveMiniPIRSensorSensor(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break;
        
        if sensor.reading():
            print('I feel someone is there, who is it?')
        else:
            print('Scanning for people...')
            
        sleep(200)

if __name__ == '__main__':
    demo()
