# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin0, pin1, pin2, sleep

class EnvironmentMonitor:
    def __init__(self, sound_pin, temperature_pin, light_pin):
        self._sound_pin = sound_pin
        self._temperature_pin = temperature_pin
        self._light_pin = light_pin
        
    def temperature(self):
        reading = self._temperature_pin.read_analog()
        return int(reading / 13.33 - 14)

    def sound_level(self):
        return (self._sound_pin.read_analog() - 511) / 100
    
    def light_level(self):
        return self._light_pin.read_analog() / 10
        
def main():
    monitor = EnvironmentMonitor(pin0, pin1, pin2)
    
    while True:
        sound = monitor.sound_level()
        temp = monitor.temperature()
        light = monitor.light_level()

        print('----------')
        print("Sound Level: {}".format(str(sound)))
        print("Temperature: {}C".format(str(temp)))
        print("Light Level: {}".format(str(light)))        
        print('----------')
        print('')
        
        sleep(2000)
        
if __name__ == '__main__':
    main()
