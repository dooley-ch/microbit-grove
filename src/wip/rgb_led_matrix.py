# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c, display, button_b
from utime import sleep_us

_DEFAULT_ADDRESS          = 0x65

_CMD_CONTINUE_DATA        = 0x81

_TWO_RGB_LED_MATRIX_VID   = 0x2886 # Vender ID of the device
_TWO_RGB_LED_MATRIX_PID   = 0x8005 # Product ID of the device

_CMD_GET_DEV_ID           = 0x00 # This command gets device ID information
_CMD_DISP_BAR             = 0x01 # This command displays LED bar
_CMD_DISP_EMOJI           = 0x02 # This command displays emoji
_CMD_DISP_NUM             = 0x03 # This command displays number
_CMD_DISP_STR             = 0x04 # This command displays string
_CMD_DISP_CUSTOM          = 0x05 # This command displays user-defined pictures
_CMD_DISP_OFF             = 0x06 # This command cleans the display
_CMD_DISP_FLASH           = 0x08 # This command displays pictures which are stored in flash
_CMD_DISP_COLOR_BAR       = 0x09 # This command displays colorful led bar
_CMD_DISP_COLOR_WAVE      = 0x0A # This command displays built-in wave animation
_CMD_DISP_COLOR_CLOCKWISE = 0x0B # This command displays built-in clockwise animation
_CMD_DISP_COLOR_ANIMATION = 0x0C # This command displays other built-in animation
_CMD_DISP_COLOR_BLOCK     = 0x0D # This command displays an user-defined color
_CMD_STORE_FLASH          = 0xA0 # This command stores frames in flash
_CMD_DELETE_FLASH         = 0xA1 # This command deletes all the frames in flash

_CMD_LED_ON               = 0xB0 # This command turns on the indicator LED flash mode
_CMD_LED_OFF              = 0xB1 # This command turns off the indicator LED flash mode
_CMD_AUTO_SLEEP_ON        = 0xB2 # This command enable device auto sleep mode
_CMD_AUTO_SLEEP_OFF       = 0xB3 # This command disable device auto sleep mode (default mode)

_CMD_DISP_ROTATE          = 0xB4 # This command setting the display orientation
_CMD_DISP_OFFSET          = 0xB5 # This command setting the display offset

_CMD_SET_ADDR             = 0xC0 # This command sets device i2c address
_CMD_RST_ADDR             = 0xC1 # This command resets device i2c address
_CMD_TEST_TX_RX_ON        = 0xE0 # This command enable TX RX pin test mode
_CMD_TEST_TX_RX_OFF       = 0xE1 # This command disable TX RX pin test mode
_CMD_TEST_GET_VER         = 0xE2 # This command use to get software version
_CMD_GET_DEVICE_UID       = 0xF1 # This command use to get chip id

_DISPLAY_ROTATE_0         = 0
_DISPLAY_ROTATE_90        = 1
_DISPLAY_ROTATE_180       = 2
_DISPLAY_ROTATE_270       = 3

_RED                      = 0x00
_ORANGE                   = 0x12
_YELLOW                   = 0x18
_GREEN                    = 0x52
_CYAN                     = 0x7F
_BLUE                     = 0xAA
_PURPLE                   = 0xC3
_PINK                     = 0xDC
_WHITE                    = 0xFE
_BLACK                    = 0xFF

class GroveRgbLedMatrix:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        self._offset_address = 0
        self._base_address = 0
        self._device_id = bytearray(0x0, 0x0, 0x0)
       
    def _write_byte(self, data):
        i2c.write(self._device_address, bytearray([data]))
        
    def _write_byte_to_address(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))
    
    def _write_2_bytes_to_address(self, address, data1, data2):
        i2c.write(self._device_address, bytearray([address, data1, data2]))
    
    def _read_bytes_at_address(self, address, num_bytes):
        i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
    
    def _read_bytes(self, num_bytes):
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
     
    # Get vendor ID of device.
    def get_device_vid(self):
        data = self._read_bytes_at_address(_CMD_GET_DEV_ID, 4)        
        return data[0] + data[1] * 256

    
    # Get product ID of device.
    def get_device_pid(self):
        data = self._read_bytes_at_address(_CMD_GET_DEV_ID, 4)        
        return data[2] + data[3] * 256
    
    # Turn on the indicator LED flash mode.
    def turn_on_led_flash(self):
        self._write_byte(_CMD_LED_ON)
    
    # Turn off the indicator LED flash mode.
    def turn_on_led_flash(self):
        self._write_byte(_CMD_LED_OFF)
    
    # Enable device auto sleep mode. Send any I2C commands will
    def enable_auto_sleep(self):
        self._write_byte(_CMD_AUTO_SLEEP_ON)
    
    # Don't need this function anymore.
    # (Wake device from sleep mode. It takes about 0.15ms.)
    def wake_device(self):
        sleep_us(200)
    
    # Disable device auto sleep mode.
    def disable_auto_sleep(self):
        self._write_byte(_CMD_AUTO_SLEEP_OFF)
    
    # Setting the display orientation.
    # This function can be used before or after display.
    # DO NOT WORK with displayColorWave(), displayClockwise(), displayColorAnimation()
    def set_display_orientation(self, value):
        self._write_byte_to_address(_CMD_DISP_ROTATE, value)
    
    # Setting the display offset of x-axis and y-axis.
    # This function can be used before or after display.
    # DO NOT WORK with displayColorWave(), displayClockwise(), displayColorAnimation(),
    # displayNumber(when number<0 or number>=10), displayString(when more than one character)
    def set_display_offset(self, value_x, value_y):
        pass
    
    # Display a bar on RGB LED Matrix.
    def display_bar(self, bar, duration_time, forever_flag = False, color = 0):
        pass
    
    # Display a colorful bar on RGB LED Matrix.
    def display_color_bar(self, bar, duration_time, forever_flag = False):
        pass
    
    # Display a wave on RGB LED Matrix.
    def display_color_wave(self, color, duration_time, forever_flag = False):
        pass
    
    # Display a clockwise(or anti-clockwise) animation on RGB LED Matrix.
    def display_clockwise(self, is_cw, is_big, duration_time, forever_flag = False):
        pass
    
    # Display other built-in animations on RGB LED Matrix.
    def display_color_animation(self, index, duration_time, forever_flag = False):
        pass
    
    # Display emoji on LED matrix.
    def display_emoji(self, emoji, duration_time, forever_flag = False):
        pass
    
    # Display a number(-32768 ~ 32767) on LED matrix.
    def display_number(self, number, duration_time, forever_flag = False, color = 0):
        pass
    
    # Display a string on LED matrix.
    def display_string(self, value, duration_time, forever_flag = False, color = 0):
        pass
    
    
    def display_frames(self, buffer, duration_time, forever_flag, frames_number):
        pass
    
    # Display color block on LED matrix with a given uint32_t rgb color.
    def display_color_block(self, rgb, duration_time, forever_flag):
        pass
    
    # Display nothing on LED Matrix.
    def stop_display(self):
        pass
    
    # Store the frames(you send to the device) to flash. It takes about 200ms.
    def store_frames(self):
        pass
    
    # Delete all the frames in the flash of device. It takes about 200ms.
    def delete_frames(self):
        pass

    # Display frames which is stored in the flash of device.
    def display_frames_from_Flash(self, duration_time, forever_flag, start, end):
        pass
    
    # Enable TX and RX pin test mode.
    def enable_test_mode(self):
        pass
    
    # disable TX and RX pin test mode.
    def disable_test_mode(self):
        pass
    
    # Get software vresion.
    def get_test_version(self):
        pass
    
    # Reset device.
    def reset_device(self):
        pass
    
    # Get device id.
    def get_device_id(self):
        pass
    
def main():
    display.clear()
    matrix = GroveRgbLedMatrix()
    
    print(matrix.get_device_vid())
    print(matrix.get_device_pid())
    
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
    display.clear()
    
if __name__ == '__main__':
    main()

