# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, sleep, display, button_b

class InfraredReflectiveSensor:
    def __init__(self, pin):
        self._pin = pin
        
    def is_black(self):
        return self._pin.read_digital() == 1
    
def main():
    sensor = InfraredReflectiveSensor(pin1)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if sensor.is_black():
            print("Black surface")
        else:
            print("White surface")
            
        sleep(2000)

if __name__ == '__main__':
    main()

