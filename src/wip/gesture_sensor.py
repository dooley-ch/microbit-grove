# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c, display, button_b

_DEFAULT_ADDRESS       = 0x73

#Register Bank select
_PAJ_BANK_SELECT       = 0xEF

#Register Bank 0
_PAJ_SUSPEND           = 0x03
_PAJ_INT_FLAG1_MASK    = 0x41
_PAJ_INT_FLAG2_MASK    = 0x42
_PAJ_INT_FLAG1         = 0x43
_PAJ_INT_FLAG2         = 0x44
_PAJ_STATE             = 0x45
_PAJ_PS_HIGH_THRESHOLD = 0x69        
_PAJ_PS_LOW_THRESHOLD  = 0x6A
_PAJ_PS_APPROACH_STATE = 0x6B
_PAJ_PS_DATA           = 0x6C
_PAJ_OBJ_BRIGHTNESS    = 0xB0
_PAJ_OBJ_SIZE_L        = 0xB1        
_PAJ_OBJ_SIZE_H        = 0xB2

#Register Bank 1
_PAJ_PS_GAIN           = 0x44
_PAJ_IDLE_S1_STEP_L    = 0x67
_PAJ_IDLE_S1_STEP_H    = 0x68    
_PAJ_IDLE_S2_STEP_L    = 0x69
_PAJ_IDLE_S2_STEP_H    = 0x6A
_PAJ_OPTOS1_TIME_L     = 0x6B    
_PAJ_OPTOS2_TIME_H     = 0x6C    
_PAJ_S1TOS2_TIME_L     = 0x6D    
_PAJ_S1TOS2_TIME_H     = 0x6E    
_PAJ_EN                = 0x72

#Gesture detection interrupt flag
_PAJ_UP                = 0x01 
_PAJ_DOWN              = 0x02
_PAJ_LEFT              = 0x04 
_PAJ_RIGHT             = 0x08
_PAJ_FORWARD           = 0x10 
_PAJ_BACKWARD          = 0x20
_PAJ_CLOCKWISE         = 0x40
_PAJ_COUNT_CLOCKWISE   = 0x80
_PAJ_WAVE              = 0x100

_INITIALIZE_REGISTER = (
    (0xEF,0x00),
    (0x37,0x07),
    (0x38,0x17),
    (0x39,0x06),
    (0x41,0x00),
    (0x42,0x00),
    (0x46,0x2D),
    (0x47,0x0F),
    (0x48,0x3C),
    (0x49,0x00),
    (0x4A,0x1E),
    (0x4C,0x20),
    (0x51,0x10),
    (0x5E,0x10),
    (0x60,0x27),
    (0x80,0x42),
    (0x81,0x44),
    (0x82,0x04),
    (0x8B,0x01),
    (0x90,0x06),
    (0x95,0x0A),
    (0x96,0x0C),
    (0x97,0x05),
    (0x9A,0x14),
    (0x9C,0x3F),
    (0xA5,0x19),
    (0xCC,0x19),
    (0xCD,0x0B),
    (0xCE,0x13),
    (0xCF,0x64),
    (0xD0,0x21),
    (0xEF,0x01),
    (0x02,0x0F),
    (0x03,0x10),
    (0x04,0x02),
    (0x25,0x01),
    (0x27,0x39),
    (0x28,0x7F),
    (0x29,0x08),
    (0x3E,0xFF),
    (0x5E,0x3D),
    (0x65,0x96),
    (0x67,0x97),
    (0x69,0xCD),
    (0x6A,0x01),
    (0x6D,0x2C),
    (0x6E,0x01),
    (0x72,0x01),
    (0x73,0x35),
    (0x74,0x00),
    (0x77,0x01),
)

_INITIALIZE_GESTURE = (
    (0xEF,0x00),
    (0x41,0x00),
    (0x42,0x00),
    (0xEF,0x00),
    (0x48,0x3C),
    (0x49,0x00),
    (0x51,0x10),
    (0x83,0x20),
    (0x9F,0xF9),
    (0xEF,0x01),
    (0x01,0x1E),
    (0x02,0x0F),
    (0x03,0x10),
    (0x04,0x02),
    (0x41,0x40),
    (0x43,0x30),
    (0x65,0x96),
    (0x66,0x00),
    (0x67,0x97),
    (0x68,0x01),
    (0x69,0xCD),
    (0x6A,0x01),
    (0x6B,0xB0),
    (0x6C,0x04),
    (0x6D,0x2C),
    (0x6E,0x01),
    (0x74,0x00),
    (0xEF,0x00),
    (0x41,0xFF),
    (0x42,0x01),
)

class GroveGestureSensor:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        
        data = self._read_register(0x00, 1)[0]
        assert data == 0x20, 'Sensor failure'
        
        for i in range(len(_INITIALIZE_REGISTER)):
            self._write_register(_INITIALIZE_REGISTER[i][0], _INITIALIZE_REGISTER[i][1])
            
        self._write_register(_PAJ_BANK_SELECT, 0)
        for i in range(len(_INITIALIZE_GESTURE)):
            self._write_register(_INITIALIZE_GESTURE[i][0], _INITIALIZE_GESTURE[i][1])
            
        self._gesture = None
        
    def _write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))

    def _read_register(self, address, num_bytes):
        i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
        
    def _read_device(self):
        lsb = self._read_register(_PAJ_INT_FLAG1, 1)[0]
        msb = self._read_register(_PAJ_INT_FLAG1 + 1, 1)[0]
        self._gesture = (msb << 8) + lsb
    
    def get_gesture(self):
        self._read_device()
        return self._gesture
    
    def get_gesture_string(self):
        self._read_device()
        
        if self._gesture == _PAJ_UP:
            return 'Up'

        elif self._gesture == _PAJ_DOWN:
           return 'Down'
        elif self._gesture == _PAJ_LEFT:
            return 'Left'    
        elif self._gesture == _PAJ_RIGHT:
            return 'Right'    
        elif self._gesture == _PAJ_FORWARD:
            return 'Forward'    
        elif self._gesture == _PAJ_BACKWARD:
            return 'Backward'
        elif self._gesture == _PAJ_CLOCKWISE:
            return 'Clockwise'    
        elif self._gesture == _PAJ_COUNT_CLOCKWISE:
            return 'AntiClockwise'    
        elif self._gesture == _PAJ_WAVE:
            return 'Wave'
        
        return 'None'
        
def demo():
    sensor = GroveGestureSensor()
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        print("Gesture: {}".format(sensor.get_gesture_string()))
        
        sleep(50)
        
if __name__ == '__main__':
    demo()
