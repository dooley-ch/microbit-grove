# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, sleep

class GroveInfraredReflectiveSensor:
    def __init__(self, pin):
        self._pin = pin
        
    def is_black(self):
        return self._pin.read_digital() == 1
    
def demo():
    sensor = GroveInfraredReflectiveSensor(pin1)
    
    while True:
        if sensor.is_black():
            print("Black surface")
        else:
            print("White surface")
            
        sleep(2000)

if __name__ == '__main__':
    demo()

