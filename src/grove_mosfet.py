# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Im my tests I needed pass 1000 as the current in order to get the full flow of a 9v battery
# need to test with multimeter for the values needed in each case

from microbit import sleep, pin16, button_b, display

class GroveMOSFET:
    def __init__(self, pin):
        self._pin = pin
        self.current(0)
        
    def current(self, value):
        self._pin.write_analog(value)

def demo():
    mosfet = GroveMOSFET(pin16)
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        print('On, the off with speed')
        mosfet.current(1000)
        sleep(3000)
        mosfet.current(0)
        sleep(3000)
        
        print('Acceleration')
        mosfet.current(0)
        sleep(1000)
        
        for i in range(0, 1000, 50):
            mosfet.current(i)
            sleep(50)
            
        for i in range(0, 1000, -50):
            mosfet.current(i)
            sleep(50)
            
        sleep(3000)
        
if __name__ == '__main__':
    demo()

