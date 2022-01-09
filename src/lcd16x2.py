# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note: While the LCD does work, it does not perform very well without an external power
# source

from microbit import i2c, sleep, display, button_b
from utime import sleep_us

_DEFAULT_ADDRESS    = 0x3E

# commands
_LCD_CLEARDISPLAY   = 0x01
_LCD_RETURNHOME     = 0x02
_LCD_ENTRYMODESET   = 0x04
_LCD_DISPLAYCONTROL = 0x08
_LCD_CURSORSHIFT    = 0x10
_LCD_FUNCTIONSET    = 0x20
_LCD_SETCGRAMADDR   = 0x40
_LCD_SETDDRAMADDR   = 0x80

# Function set flags
_LCD_2LINE           = 0x08

# flags for display on/off control
_LCD_DISPLAYON       = 0x04
_LCD_DISPLAYOFF      = 0x00
_LCD_CURSORON        = 0x02
_LCD_CURSOROFF       = 0x00
_LCD_BLINKON         = 0x01
_LCD_BLINKOFF        = 0x00

# flags for display/cursor shift
_LCD_DISPLAYMOVE = 0x08
_LCD_MOVERIGHT = 0x04
_LCD_MOVELEFT = 0x00

# flags for display entry mode
# _LCD_ENTRYRIGHT      =  0x00
_LCD_ENTRYLEFT       = 0x02
_LCD_ENTRYSHIFTINCREMENT = 0x01
_LCD_ENTRYSHIFTDECREMENT  = 0x00

class Lcd16x2():
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        
        self._display_function = _LCD_DISPLAYON | _LCD_2LINE
        sleep_us(50000)
        
        self.command(_LCD_FUNCTIONSET | self._display_function)
        sleep_us(4500)
        self.command(_LCD_FUNCTIONSET | self._display_function)
        sleep_us(150)
        self.command(_LCD_FUNCTIONSET | self._display_function)
        
        self._display_control = _LCD_DISPLAYON | _LCD_CURSOROFF | _LCD_BLINKOFF
        self.display(True)
        
        self.clear()
        
        self._display_mode = _LCD_ENTRYLEFT | _LCD_ENTRYSHIFTDECREMENT
        self.command(_LCD_ENTRYMODESET | self._display_mode)

    def _write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))

    def command(self, value):
        assert value >= 0 and value < 256
        self._write_register(_LCD_SETDDRAMADDR, value)

    def write_character(self, value):
        assert value >= 0 and value < 256
        self._write_register(_LCD_SETCGRAMADDR, value)

    def write(self, value):
        value = str(value)
        for char in value:
            self.write_character(ord(char))
            sleep_us(200)

    def set_cursor(self, col, row):
        col = (col | 0x80) if row == 0 else (col | 0xc0)
        self.command(col)

    def display(self, state):
        if state:
            self._display_control |= _LCD_DISPLAYON
            self.command(0x08  | self._display_control)
        else:
            self._display_control &= ~_LCD_DISPLAYON
            self.command(0x08  | self._display_control)

    def clear(self):
        self.command(_LCD_CLEARDISPLAY)
        sleep_us(2000)

    def home(self):
        self.command(_LCD_CLEARDISPLAY)
        sleep_us(2000)
        
    def autoscroll(self):
        self._display_mode |= _LCD_ENTRYSHIFTINCREMENT
        self.command(_LCD_ENTRYMODESET | self._display_mode)

    def no_autoscroll(self):
        self._display_mode &= ~_LCD_ENTRYSHIFTINCREMENT
        self.command(_LCD_ENTRYMODESET | self._display_mode);

    def blink(self):
        self._display_control |= _LCD_BLINKON
        self.command(_LCD_DISPLAYCONTROL | self._display_control);
        
    def no_blink(self):
        self._display_control &= ~_LCD_BLINKON
        self.command(_LCD_DISPLAYCONTROL | self._display_control);
        sleep_us(2000)
       
    def cursor(self):
        self._display_control |= _LCD_CURSORON
        self.command(_LCD_DISPLAYCONTROL | self._display_control);
        
    def no_cursor(self):
        self._display_control &= ~_LCD_CURSORON
        self.command(_LCD_DISPLAYCONTROL | self._display_control);
        sleep_us(2000)
       
    def scroll_display_left(self):
        self.command(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVELEFT);
        sleep_us(2000)
      
    def scroll_display_right(self):
        self.command(_LCD_CURSORSHIFT | _LCD_DISPLAYMOVE | _LCD_MOVERIGHT);
        sleep_us(2000)
        
    def left_to_right(self):
        self._display_mode |= _LCD_ENTRYLEFT;
        self.command(_LCD_ENTRYMODESET | self._display_mode);
        
    def right_to_left(self):
        self._display_mode &= ~_LCD_ENTRYLEFT;
        self.command(_LCD_ENTRYMODESET | self._display_mode);

def main():
    board = Lcd16x2()

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        board.clear()
        board.write('Hello World')
        
        board.set_cursor(0, 1)
        for i in range(20):
            board.set_cursor(0, 1)
            board.write(str(i))
            sleep(500)
            
        sleep(1000)
            
if __name__ == '__main__':
    main()
    