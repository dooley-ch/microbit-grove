# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import i2c, sleep, Image

_DEFAULT_ADDRESS = 0x3C

_INIT_COMMANDS = [
        [0xAE],
        [0xA4],
        [0xD5, 0xF0],
        [0xA8, 0x3F],
        [0xD3, 0x00],
        [0 | 0x0],
        [0x8D, 0x14],
        [0x20, 0x00],
        [0x21, 0, 127],
        [0x22, 0, 63],
        [0xa0 | 0x1],
        [0xc8],
        [0xDA, 0x12],
        [0x81, 0xCF],
        [0xd9, 0xF1],
        [0xDB, 0x40],
        [0xA6],
        [0xd6, 1],
        [0xaf]]

class OledSSD1306:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        self._buffer = bytearray(513)
        self._buffer[0] = 0x40
        self._zoom = 1
 
        for cmd in _INIT_COMMANDS:
            self._write_registery(cmd)

        self.clear()
        
    def _write_registery(self, value):
        i2c.write(self._device_address, b'\x00' + bytearray(value))

    def _set_position(self, column = 0, page = 0):
        self._write_registery([0xB0 | page]) 

        c1, c2 = column * 2 & 0x0F, column >> 3
        self._write_registery([0x00 | c1])
        self._write_registery([0x10 | c2])
        
    def _set_zoom(self, value):
        if self._zoom != value:
            self._write_registery([0xD6, value])
            self._write_registery([0xA7 - value])
            
            self._zoom = value
     
    def _write_buffer(self):
        self._set_zoom(1)
        self._set_position()
        i2c.write(self._device_address, self._buffer)
        
    def clear(self): 
        self._set_position()
        for i in range(1, 513):
            self._buffer[i] = 0
        self._write_buffer()
   
    def blink(self, time = 1000):
        for c in ([0xae], [0xaf]):
            self._write_registery(c)
            sleep(time / 2)

    def pulse(self, time=500):
        per_step = time / 25
        r = [[250, 0, -10], [0, 250, 10]]
        
        for (x, y, z) in r:
            for i in range(x, y, z):
                self._write_registery([0x81, i])
                sleep(per_step)
                
        self._write_registery([0x81, 0xcf])

    def string(self, x, y, value, draw=1):
        for i in range(0, min(len(value), 12 - x)):
            for c in range(0, 5):
                col = 0
                for r in range(1, 6):
                    p = Image(value[i]).get_pixel(c, r - 1)
                    col = col | (1 << r) if (p != 0) else col
                ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
                self._buffer[ind], self._buffer[ind + 1] = col, col  
        if draw == 1:
            self._set_zoom(1)
            self._set_position((x) * 5, (y))
            ind0 = x * 10 + y * 128 + 1 
            i2c.write(self._device_address, b'\x40' + self._buffer[ind0:ind + 1]) 
      
def main():   
    i2c.init()
    display = OledSSD1306()
    
    display.string(4, 1, "Hello")
    display.string(4, 2, "World")
    display.pulse()

if __name__ == '__main__':
    main()
    