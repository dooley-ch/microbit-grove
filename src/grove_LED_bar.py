# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin1, pin15, sleep
import random

_LOW                 = 0
_HIGH                = 1
_LED_TURN_OFF        = 0x00
_LED_FULL_BRIGHTNESS = 0xFF
_MAX_LED_COUNT       = 10

class GroveLEDBar:
    def __init__(self, clock_pin, data_pin, red_2_green = True):
        self._clock_pin = clock_pin
        self._data_pin = data_pin
        self._red_2_green = red_2_green
        self._leds = [_LED_TURN_OFF, _LED_TURN_OFF, _LED_TURN_OFF, _LED_TURN_OFF, _LED_TURN_OFF,
                     _LED_TURN_OFF, _LED_TURN_OFF, _LED_TURN_OFF, _LED_TURN_OFF,_LED_TURN_OFF]
        
        self._send()

    def set_green_2_red(self, red_2_green):
        self._red_2_green = red_2_green
        self.set_bits(self._state)
    
    def set_level(self, level):
        pass
    
    def set_led(self, led, state):
        pass
    
    def toggle_led(self, led):
        if led < 1:
            led = 1
        elif led > _MAX_LED_COUNT:
            led = _MAX_LED_COUNT
        
        led = led - 1
        
        if self._leds[led]:
            self._leds[led] = _LED_TURN_OFF
        else:
            self._leds[led] = _LED_FULL_BRIGHTNESS
        
        self._send()
    
    def set_bits(self, bits):
        values = bits.to_bytes(10, 'big')
        
        for i in range(_MAX_LED_COUNT):
            self._leds[i] = values[i]
        
        self._send()
    
    def get_bits(self):
        return bytearray(self._leds)

    def _latch_data(self):
        pass
    
    def _send(self):
        bits = self.get_bits()
        print("Data to send: {}".format(str(bits)))
    
def demo():
    for loops in range(1):
        print("Test 1) Initialise - red to green")
        bar = GroveLEDBar(pin1, pin15)
        sleep(500)
        
        print("Test 2) Set level")
        for i in range(11):
            bar.set_level(i)
            sleep(200)
        sleep(300)
        
        bar.set_level(8)
        sleep(500)
        
        bar.set_level(2)
        sleep(500)
        
        bar.set_level(5)
        sleep(500)        
        
        print("Test 3) Switch on/off a single LED")
        bar.set_led(10, 1)
        sleep(500)
        
        bar.set_led(9, 1)
        sleep(500)

        bar.set_led(8, 1)
        sleep(500)

        bar.set_led(1, 0)
        sleep(500)
        
        bar.set_led(2, 0)
        sleep(500)
        
        bar.set_led(3, 0)
        sleep(500)
        
        print("Test 4) Toggle a single LED")
        bar.toggle_led(1)
        sleep(500)

        bar.toggle_led(2)
        sleep(500)
 
        bar.toggle_led(9)
        sleep(500)
        
        bar.toggle_led(1)
        sleep(500)
        
        print ("Test 5) Set state - control all leds with 10 bits")
        for i in range(32):
            bar.set_bits(i)
            sleep(200)
        sleep(300)
        
        
        print ("Test 6) Get current state")
        state = bar.get_bits()
        
        print ("with first 5 leds lit, the state should be 31 or 0x1F")
        print (state)
        sleep(500)
        
        if state != None:
            state = state << 5
            print ("the state should now be 992 or 0x3E0")
            print (state)
            sleep(500)

        print ("Test 7) Set state - save the state we just modified")

        bar.set_bits(state)
        sleep(500)


        print ("Test 8) Swap orientation - green to red (currently green to red)")
        bar.set_green_2_red(False)
        sleep(2000)

        print ("and back to green to red")
        bar.set_green_2_red(True)
        sleep(500)        
        
        print ("Test 9) Set level, again")
        for i in range(11):
            bar.set_level(i)
            sleep(200)
        sleep(300)

        print ("Test 10) Set a single LED, again")
        bar.set_led(1, 0)
        sleep(500)

        bar.set_led(3, 0)
        sleep(500)

        bar.set_led(5, 0)
        sleep(500)

        print ("Test 11) Toggle a single LED, again")
        bar.toggle_led(2)
        sleep(500)

        bar.toggle_led(4)
        sleep(500)
        
        print ("Test 12) Get state")
        state = bar.get_bits()

        print ("the last 5 LEDs are lit, so the state should be 992 or 0x3E0")
        print (state)
        sleep(500)
        
        if state != None:
            state = state << 5
            print ("the state should now be 31 or 0x1F")
            print (state)
            sleep(500)

        print ("Test 13) Set state, again")
        bar.set_bits(state)
        sleep(500)

        print ("Test 14) Step")
        for i in range(11):
            bar.set_level(i)
            sleep(200)
        sleep(300)


        print ("Test 15) Bounce")
        bar.set_level(2)

        # get the current state (which is 0x3)
        state = bar.get_bits()

        # bounce to the right
        if state != None:
            for i in range(9):
                state <<= 1;
                bar.set_bits(state)
                sleep(200)

        # bounce to the left
        if state != None:
            for i in range(9):
                state >>= 1;
                bar.set_bits(state)
                sleep(200)
        sleep(300)


        print ("Test 16) Random")
        for i in range(21):
            state = random.randint(0,1023)
            bar.set_bits(state)
            sleep(200)
        sleep(300)


        print ("Test 17) Invert")
        # set every 2nd LED on - 341 or 0x155
        state = 341
        for i in range(5):
            bar.set_bits(state)
            sleep(200)

            # bitwise XOR all 10 LEDs on with the current state
            state = 0x3FF ^ state

            bar.set_bits(state)
            sleep(200)
        sleep(300)

        print ("Test 18) Walk through all possible combinations")
        for i in range(1024):
            bar.set_bits(i)
            sleep(100)
        sleep(400)
        
        print("")
        
    print("Demo done")

if __name__ == '__main__':
    obj = GroveLEDBar(pin1, pin15)
    obj.toggle_led(1)
    obj.toggle_led(2)
    obj.toggle_led(1)
    
    obj.set_bits(0x3ff)
    
    print("Done")
