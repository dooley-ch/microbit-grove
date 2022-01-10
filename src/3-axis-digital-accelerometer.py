# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c, display, button_b

_DEFAULT_ADDRESS = 0x19

# _LIS3DHTR Register Map
_LIS3DHTR_REG_WHOAMI                 = 0x0F # Who Am I Register
_LIS3DHTR_REG_CTRL1                  = 0x20 # Control Register-1
_LIS3DHTR_REG_CTRL2                  = 0x21 # Control Register-2
_LIS3DHTR_REG_CTRL3                  = 0x22 # Control Register-3
_LIS3DHTR_REG_CTRL4                  = 0x23 # Control Register-4
_LIS3DHTR_REG_CTRL5                  = 0x24 # Control Register-5
_LIS3DHTR_REG_CTRL6                  = 0x25 # Control Register-6
_LIS3DHTR_REG_REFERENCE              = 0x26 # Reference
_LIS3DHTR_REG_STATUS                 = 0x27 # Status Register
_LIS3DHTR_REG_OUT_X_L                = 0x28 # X-Axis LSB
_LIS3DHTR_REG_OUT_X_H                = 0x29 # X-Axis MSB
_LIS3DHTR_REG_OUT_Y_L                = 0x2A # Y-Axis LSB
_LIS3DHTR_REG_OUT_Y_H                = 0x2B # Y-Axis MSB
_LIS3DHTR_REG_OUT_Z_L                = 0x2C # Z-Axis LSB
_LIS3DHTR_REG_OUT_Z_H                = 0x2D # Z-Axis MSB
 
# Accl Datarate configuration
_LIS3DHTR_ACCL_DR_PD                 = 0x00 # Power down mode
_LIS3DHTR_ACCL_DR_1                  = 0x10 # ODR = 1 Hz
_LIS3DHTR_ACCL_DR_10                 = 0x20 # ODR = 10 Hz
_LIS3DHTR_ACCL_DR_25                 = 0x30 # ODR = 25 Hz
_LIS3DHTR_ACCL_DR_50                 = 0x40 # ODR = 50 Hz
_LIS3DHTR_ACCL_DR_100                = 0x50 # ODR = 100 Hz
_LIS3DHTR_ACCL_DR_200                = 0x60 # ODR = 200 Hz
_LIS3DHTR_ACCL_DR_400                = 0x70 # ODR = 400 Hz
_LIS3DHTR_ACCL_DR_1620               = 0x80 # ODR = 1.620 KHz
_LIS3DHTR_ACCL_DR_1344               = 0x90 # ODR = 1.344 KHz
 
# Accl Data update & Axis configuration
_LIS3DHTR_ACCL_LPEN                  = 0x00 # Normal Mode, Axis disabled
_LIS3DHTR_ACCL_XAXIS                 = 0x04 # X-Axis enabled
_LIS3DHTR_ACCL_YAXIS                 = 0x02 # Y-Axis enabled
_LIS3DHTR_ACCL_ZAXIS                 = 0x01 # Z-Axis enabled
 
# Acceleration Full-scale selection
_LIS3DHTR_BDU_CONT                   = 0x00 # Continuous update, Normal Mode, 4-Wire Interface
_LIS3DHTR_BDU_NOT_CONT               = 0x80 # Output registers not updated until MSB and LSB reading
_LIS3DHTR_ACCL_BLE_MSB               = 0x40 # MSB first
_LIS3DHTR_ACCL_RANGE_16G             = 0x30 # Full scale = +/-16g
_LIS3DHTR_ACCL_RANGE_8G              = 0x20 # Full scale = +/-8g
_LIS3DHTR_ACCL_RANGE_4G              = 0x10 # Full scale = +/-4g
_LIS3DHTR_ACCL_RANGE_2G              = 0x00 # Full scale = +/-2g, LSB first
_LIS3DHTR_HR_DS                      = 0x00 # High-Resolution Disabled
_LIS3DHTR_HR_EN                      = 0x08 # High-Resolution Enabled
_LIS3DHTR_ST_0                       = 0x02 # Self Test 0
_LIS3DHTR_ST_1                       = 0x04 # Self Test 1
_LIS3DHTR_SIM_3                      = 0x01 # 3-Wire Interface

class ThreeAxisDigitalAccelerometer:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS

        self._select_datarate()
        self._select_data_config()
        sleep(0.1)
        
    def _write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))
    
    def _read_register(self, address, num_bytes):
        i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
    
    def _select_datarate(self):
        data = (_LIS3DHTR_ACCL_DR_10 | _LIS3DHTR_ACCL_XAXIS | _LIS3DHTR_ACCL_YAXIS | _LIS3DHTR_ACCL_ZAXIS)
        self._write_register(_LIS3DHTR_REG_CTRL1, data)
 
    def _select_data_config(self):
        data = (_LIS3DHTR_ACCL_RANGE_2G | _LIS3DHTR_BDU_CONT | _LIS3DHTR_HR_DS)
        self._write_register(_LIS3DHTR_REG_CTRL4, data)
    
    def read(self):
        data0 = self._read_register(_LIS3DHTR_REG_OUT_Y_L, 1)[0]
        data1 = self._read_register(_LIS3DHTR_REG_OUT_Y_H, 1)[0]
        
        xAccl = data1 * 256 + data0
        if xAccl > 32767 :
            xAccl -= 65536
        xAccl /= 16000
       
        data0 = self._read_register(_LIS3DHTR_REG_OUT_Y_L, 1)[0]
        data1 = self._read_register(_LIS3DHTR_REG_OUT_Y_H, 1)[0]
       
        yAccl = data1 * 256 + data0
        if yAccl > 32767 :
            yAccl -= 65536
        yAccl /= 16000

        data0 = self._read_register(_LIS3DHTR_REG_OUT_Z_L, 1)[0]
        data1 = self._read_register(_LIS3DHTR_REG_OUT_Z_H, 1)[0]
 
        zAccl = data1 * 256 + data0
        if zAccl > 32767 :
            zAccl -= 65536
        zAccl /= 16000

        return {'x' : xAccl, 'y' : yAccl, 'z' : zAccl}

def main():
    sensor = ThreeAxisDigitalAccelerometer()
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        accl = sensor.read()

        print(" Acceleration in X-Axis : {}".format(str(accl['x'])))
        print(" Acceleration in Y-Axis : {}".format(str(accl['y'])))
        print(" Acceleration in Z-Axis : {}".format(str(accl['z'])))
        print("")
    
        sleep(500)
        
if __name__ == '__main__':
    main()
