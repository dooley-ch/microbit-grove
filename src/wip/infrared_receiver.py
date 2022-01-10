# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Works with the Sparkfun remote control: https://www.sparkfun.com/products/14865

from microbit import pin0, sleep
from utime import sleep_us

_VALID_KEYS = ['629D', '22DD', '02FD', 'C23D', '9867', '30CF', '18E7', '7A85', '38C7']

class GroveInfraredReceiver:
    def __init__(self, pin):
        self._pin = pin
        self._last_value = None
        
    def _read_on(self):
        data = 0
        
        while self._pin.read_analog() < 500 and data < 500:
            data += 1
            
        return data
    
    def _read_off(self):
        data = 0
        
        while self._pin.read_analog() > 500 and data < 500:
            data += 1
            
        return data
    
    def _wait_for_signal(self):
        while self._pin.read_analog() > 500:
            pass
      
    def _read(self):
        while True:
            self._wait_for_signal()
            
            c1 = 0
            c2 = 0
            data = 0
            
            while c1 < 25 and c2 < 25:
                c1 = self._read_on();
                c2 = self._read_off();
            
            for i in range(32):
                c1 = self._read_on();
                c2 = self._read_off();
                
                data = data + data
                
                if c2 > 10:
                    data = data + 1
            
            data = str(hex(data)).upper()
            
            data = data[-4:]
            if data in _VALID_KEYS:
                break
            
        self._last_value = data
        
    def value(self):
        self._read()
        return self._last_value
    
def demo():
    receiver = GroveInfraredReceiver(pin0)
    
    while True:        
        value = receiver.value()
        print(value)
        sleep_us(100)

if __name__ == '__main__':
    demo()
