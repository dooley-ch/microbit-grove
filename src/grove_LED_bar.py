# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin15, pin16, sleep, display, button_b
from utime import sleep_ms

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
        
        self._leds = bytearray(_MAX_LED_COUNT)
        for i in range(_MAX_LED_COUNT):
            self._leds[i] = _LED_TURN_OFF

        self._send()

    def set_green_2_red(self, red_2_green):
        if self._red_2_green != red_2_green:
            self._red_2_green = red_2_green
            self._send()
    
    def set_led(self, led, brightness):
        led = max(1, min(_MAX_LED_COUNT, led))
        led -= 1
        self._leds[led] = brightness 
        
        self._send()
        
    def toggle_led(self, led):
        max(1, min(_MAX_LED_COUNT, led))
        
        led -= 1
        
        if self._leds[led]:
            self._leds[led] = _LED_TURN_OFF
        else:
            self._leds[led] = _LED_FULL_BRIGHTNESS
        
        self._send()
    
    def set_bits(self, value):
        assert len(value) == 10, 'Invalue bit string lenght must be 10'
        
        index = 0
        
        for ch in value:
            if ch == '0':
               self._leds[index] = _LED_TURN_OFF 
            elif ch == '1':
               self._leds[index] = _LED_FULL_BRIGHTNESS
            else:
                raise ValueError("Unsupported value in bit array: {}".format(ch))
       
            index += 1
            
        self._send()
    
    def get_bits(self):
        return self._leds

    def _latch_data(self):
        self._data_pin.write_digital(_LOW);
        self._clock_pin.write_digital(_HIGH);
        self._clock_pin.write_digital(_LOW);
        self._clock_pin.write_digital(_HIGH);
        self._clock_pin.write_digital(_LOW);
        sleep_ms(240);
        
        self._data_pin.write_digital(_HIGH);
        self._data_pin.write_digital(_LOW);
        self._data_pin.write_digital(_HIGH);
        self._data_pin.write_digital(_LOW);
        self._data_pin.write_digital(_HIGH);
        self._data_pin.write_digital(_LOW);
        self._data_pin.write_digital(_HIGH);
        self._data_pin.write_digital(_LOW);
        sleep_ms(1);
        
        self._clock_pin.write_digital(_HIGH);
        self._clock_pin.write_digital(_LOW);
    
    def _send_byte(self, value):
        clock_value = _LOW
        
        for i in range(16):
            if value & 0x8000:
                data = _HIGH
            else:
                data = _LOW
                
            self._data_pin.write_digital(data)
            self._clock_pin.write_digital(clock_value)
            
            if clock_value == _LOW:
                clock_value = _HIGH
            else:
                clock_value = _LOW
                
            value <<= 1
            
    
    def _send(self):
        if self._red_2_green:
            self._send_byte(0x00)
            
            for value in reversed(self._leds):
                self._send_byte(value)
                
            for i in range(2):
                self._send_byte(0x00)
        else:
            for value in self._leds:
                self._send_byte(value)
                
        self._latch_data()
        
def demo():
    led_bar = GroveLEDBar(pin16, pin15)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        
if __name__ == '__main__':
    obj = GroveLEDBar(pin16, pin15)
    
    # Turn off leds
    obj.set_bits('0000000000')
    sleep(100)
    
    # Turn on all leds
    obj.set_bits('1111111111')
    sleep(1000)
  
    # Turn on led 1
    obj.set_bits('1000000000')
    sleep(1000)
    
    # Turn on led 1 and 3
    obj.set_bits('1010000000')
    sleep(1000)
    
    # Turn on led 1, 3, 5, 7, 9
    obj.set_bits('1010101010')
    sleep(1000)
    
    # Turn on led 2, 4, 6, 8, 10
    obj.set_bits('0101010101')
    sleep(1000)
    
    # Turn on led 1, 2, 3, 4, 5
    obj.set_bits('1111100000')
    sleep(1000)

    # Turn on led 6, 7, 8, 9, 10
    obj.set_bits('0000011111')
    sleep(1000)

    sleep(2000)