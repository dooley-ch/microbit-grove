# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Displaying characters on a segment can be problematic, check how they will luck before using them

from microbit import *
from utime import sleep_us
from math import fabs

_HIGH           = 1
_LOW            = 0

_STARTADDR      = 0xC0
_ADDR_AUTO      = 0x40
_ADDR_FIXED     = 0x44

_BRIGHTNESS_ADJ = 0x88

_BRIGHT_DARKEST = 0
_BRIGHT_TYPICAL = 2
_BRIGHTEST      = 7

_POINT_ON       = 1
_POINT_OFF      = 0
_POINT_FLAG     = 0x80

_SPACE_CHAR      = 0x00
_MINUS_CHAR      = 0x40
_DEGREE_CHAR     = 0x63
_DASH_CHAR       = 0x08
_NUMBER_MAP      = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F')
_CHARS_MAP       = bytearray(b'\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

class Grove4DigitDisplay(object):
    def __init__(self, data_pin, clock_pin, brightness = _BRIGHT_TYPICAL):
        self._clock_pin = clock_pin
        self._data_pin = data_pin
        self._brightness = max(_BRIGHT_DARKEST, min(brightness, _BRIGHTEST))
        self._point_flag = _POINT_OFF
        self._signal_data_command()
        self._send_display_control()
        
    def _start(self):
        self._data_pin.write_digital(_LOW)
        self._clock_pin.write_digital(_LOW)

    def _stop(self):
        self._data_pin.write_digital(_LOW)
        self._clock_pin.write_digital(_HIGH)
        self._data_pin.write_digital(_HIGH)

    def _signal_data_command(self):
        self._start()
        self._write_byte(_ADDR_AUTO)
        self._stop()

    def _send_display_control(self):
        self._start()
        self._write_byte(_BRIGHTNESS_ADJ | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self._data_pin.write_digital((b >> i) & 1)
            self._clock_pin.write_digital(_HIGH)
            self._clock_pin.write_digital(_LOW)
            
        self._clock_pin.write_digital(_LOW)
        self._clock_pin.write_digital(_HIGH)
        self._clock_pin.write_digital(_LOW)

    def _update_display(self, segments, pos = 0):
        self._signal_data_command()
        self._start()
        self._write_byte(_STARTADDR | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._send_display_control()

    def get_point_flag(self):
        return self._point
    
    def set_point_flag(self, value):
        if value:
            self._point_flag = _POINT_ON
        else:
            self._point_flag = _POINT_OFF
            
    def get_brightness(self):
        return self._brightness
    
    def set_brightness(self, value):
        self._brightness  = max(_BRIGHT_DARKEST, min(value, _BRIGHTEST))
        
        self._signal_data_command()
        self._send_display_control()
        
    def encode_string(self, value):
        data = bytearray(len(value))
        for i in range(len(value)):
            data[i] = self.encode_charecter(value[i])
        return data

    def encode_charecter(self, value):
        char = ord(value)
        
        # Special characters
        if char == 32:
            return _SPACE_CHAR
        if char == 42:
            return _DEGREE_CHAR
        if char == 45:
            return _DASH_CHAR
        
        # ASCII characters
        if char >= 65 and char <= 90:
            return _CHARS_MAP[o - 65]
        if char >= 97 and char <= 122:
            return _CHARS_MAP[char - 97] # lowercase a-z
        
        # Numbers
        if char >= 48 and char <= 57:
            return _NUMBER_MAP[char - 48]
        
        raise ValueError('Character not supported: ' + value)

    def display_number(self, value, decimal = 0, show_minus = False, leading_zeros = False):
        value = (round(fabs(value) * pow(10, decimal)))
        value = max(-999, min(value, 9999))
        number = "{:>4}".format(value)
        
        if leading_zeros:
            number = number.replace(' ', '0')
        
        segments = self.encode_string(number)
        
        if self._point_flag:
            segments[1] |= _POINT_FLAG
            
        if abs(value) < 999 and show_minus:
            segments[0] = _MINUS_CHAR
            
        self._update_display(segments)
        
    def display_scrolling_string(self, value, delay_loop = 500):
        value = self.encode_string(value)

        data = [0] * 8
        
        data[4:0] = list(value)
        for i in range(len(value) + 5):
            self._update_display(data[0+i:4+i])
            sleep(delay_loop)

    def display_string(self, value):
        data = self.encode_string(value)
        
        if len(data) > 1 and self._point_flag:
            data[1] |= _POINT_FLAG
            
        self._update_display(data[:4])        
        
    def display_clear(self):
        self.set_point_flag(False)
        self.display_string('    ')
        
    def display_time(self, hours, minutes):
        self.set_point_flag(True)
        hours = min(hours, 23)
        minutes = min(minutes, 59)
        
        hours = "{:>2}".format(hours)
        minutes = "{:>2}".format(minutes)
        
        time = "{:>2}{:>2}".format(hours, minutes)
        time = time.replace(' ', '0')
        
        self.display_string(time)
        
    def display_temperature(self, value, fahrenheit = False):
        data = value
        if data < -9 or data > 99:
            raise ValueException('Temperature value out of range')
        
        data = "{:>2}".format(data)
        
        data = data + '*'
        
        if fahrenheit:
            data = data + 'F'
        else:
            data = data + 'C'
            
        segments = self.encode_string(data)

        if value < 0:
            segments[0] = _MINUS_CHAR
        
        self.set_point_flag(False)
        self._update_display(segments)
        
def demo():
    display = Grove4DigitDisplay(pin15, pin16)

    while True:
        if button_b.was_pressed():
            break
        
        # Clear screen
        display.display_clear()
        sleep(1000)
        
        # Show 88:88
        display.set_point_flag(True)
        display.display_string('8888')
        sleep(2000)
              
        # Show 8888
        display.set_point_flag(False)
        display.display_string('8888')
        sleep(2000)
        
        # Show 145 with leading space
        display.display_number(145, 0)
        sleep(2000)
        
        # Show 145 with leading space
        display.display_number(145, 0, False, True)
        sleep(2000)
        
        # Display 1.45
        display.set_point_flag(True)
        display.display_number(1.45, 2)
        sleep(2000)

        # Show -145 with leading space
        display.set_point_flag(False)
        display.display_number(145, 0, True)
        sleep(2000)

        # Display time 09:01
        display.display_time(9, 1)
        sleep(2000)
        
        # Display Temperature
        display.display_temperature(23)
        sleep(2000)
        
        # Check numbers
        print()
        display.display_scrolling_string('0123456789')
        sleep(2000)
        
        # Check upper case letters
        print()
        display.display_scrolling_string('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1000)
        sleep(2000)

        # Check lower case letters
        print()
        display.display_scrolling_string('abcdefghijklmnopqrstuvwxyz', 1000)
        sleep(2000)
        
        # Brightness
        display.set_point_flag(True)
        display.display_string('9999')
        sleep(2000)
        
        display.set_brightness(_BRIGHT_DARKEST)
        display.set_point_flag(True)
        display.display_string('9999')
        sleep(2000)
        
        display.set_brightness(_BRIGHT_TYPICAL)
        display.set_point_flag(True)
        display.display_string('9999')
        sleep(2000)
        
        display.set_brightness(_BRIGHTEST)
        display.set_point_flag(True)
        display.display_string('9999')
        sleep(2000)        
     
        display.set_brightness(_BRIGHT_TYPICAL)
     
if __name__ == '__main__':
    demo()
