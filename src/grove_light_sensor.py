# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# https://www.seeedstudio.com/Grove-Light-Sensor-v1-2-LS06-S-phototransistor.html

# This sensor needs an analog in pin: P0, P1, P2

from microbit import pin0, sleep, button_b, display

class GroveLightSensor:
    def __init__(self, pin):
        self._pin = pin

    def value(self):
        return self._pin.read_analog()

def demo():
    sensor = GroveLightSensor(pin0)
    
    while True:
        if button_b.was_pressed():
            break
        
        print("Light reading {}".format(str(sensor.value())))
        sleep(5000)
    

if __name__ == '__main__':
    demo()
