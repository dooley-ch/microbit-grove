# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, sleep
import neopixel
from random import randint
from utime import sleep_ms

_NUMBER_OF_PIXELS = 60

class GroveNeopixels:
    def __init__(self, pin):
        self._np = neopixel.NeoPixel(pin, _NUMBER_OF_PIXELS)
        self._np.clear()

    def color_wipe(self, red, green, blue, wait = 50):
        for i in range(_NUMBER_OF_PIXELS):
            self._np[i] = (red, green, blue)
            self._np.show()
            sleep_ms(wait)
   
    def theater_chase(self, red, green, blue, wait = 50, iterations = 10):
        for j in range(iterations):
            for q in range(3):
                for i in range(0, _NUMBER_OF_PIXELS, 3):
                    self._np[i + q] = (red, green, blue)
                self._np.show()
                sleep_ms(wait)
                for i in range(0, _NUMBER_OF_PIXELS, 3):
                    self._np[i + q] = (0, 0, 0)
       
    def rainbow(self, wait = 20, iterations = 1):
        for j in range(256 * iterations):
            for i in range(_NUMBER_OF_PIXELS):
                self._np[i] = self._wheel((i + j) & 255)
            self._np.show()
            sleep_ms(wait)
   
    def rainbow_cycle(self, wait = 20, iterations = 5):
        for j in range(256 * iterations):
            for i in range(_NUMBER_OF_PIXELS):
                self._np[i] = self._wheel((int(i * 256 / _NUMBER_OF_PIXELS) + j) & 255)
            self._np.show()
            sleep_ms(wait)
 
    def theater_chase_rainbow(self, wait = 50):
        for j in range(256):
            for q in range(3):
                for i in range(0, _NUMBER_OF_PIXELS, 3):
                    self._np[i + q] = self._wheel(((i+j) % 255))
                self._np.show()
                sleep_ms(wait)
                for i in range(0, _NUMBER_OF_PIXELS, 3):
                    self._np[i + q] = (0, 0, 0)
 
    def clear(self):
        self._np.clear()
        
    def _wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
        
def demo():
    lights = GroveNeopixels(pin1)    
    
    print('Press Ctrl-C to quit.')
    print('')
    
    while True:
        print ('Color wipe animations.')
        lights.color_wipe(255, 0, 0)  # Red wipe
        lights.color_wipe(0, 255, 0)  # Blue wipe
        lights.color_wipe(0, 0, 255)  # Green wipe
        sleep(1000)
        lights.clear()

        print ('Theater chase animations.')
        lights.theater_chase(127, 127, 127)  # White theater chase
        lights.theater_chase(127,   0,   0)  # Red theater chase
        lights.theater_chase(  0,   0, 127)  # Blue theater chase
        sleep(1000)
        lights.clear()
        
        print ('Rainbow animations.')
        lights.rainbow(20, 3)
        lights.rainbow_cycle()
        lights.theater_chase_rainbow()
        
if __name__ == '__main__':
    demo()
