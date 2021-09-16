# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c
from ustruct import unpack as unp

_DEFAULT_ADDRESS = 0x29

_TSL2561_CONTROL    = 0x80
_TSL2561_TIMING     = 0x81
_TSL2561_INTRRUPT   = 0x86
_TSL2561_CHANNAL_0L = 0x8C
_TSL2561_CHANNAL_0H = 0x8D
_TSL2561_CHANNAL_1L = 0x8E
_TSL2561_CHANNAL_1H = 0x8F

_LUX_SCALE          = 14       # scale by 2^14
_RATIO_SCALE        = 9        # scale ratio by 2^9
_CH_SCALE           = 10       # scale channel values by 2^10
_CH_SCALE_TINT0     = 0x7517   # 322/11 * 2^CH_SCALE
_CH_SCALE_TINT1     = 0x0fe7   # 322/81 * 2^CH_SCALE

_K1T = 0x0040   # 0.125 * 2^RATIO_SCALE
_B1T = 0x01f2   # 0.0304 * 2^LUX_SCALE
_M1T = 0x01be   # 0.0272 * 2^LUX_SCALE
_K2T = 0x0080   # 0.250 * 2^RATIO_SCA
_B2T = 0x0214   # 0.0325 * 2^LUX_SCALE
_M2T = 0x02d1   # 0.0440 * 2^LUX_SCALE
_K3T = 0x00c0   # 0.375 * 2^RATIO_SCALE
_B3T = 0x023f   # 0.0351 * 2^LUX_SCALE
_M3T = 0x037b   # 0.0544 * 2^LUX_SCALE
_K4T = 0x0100   # 0.50 * 2^RATIO_SCALE
_B4T = 0x0270   # 0.0381 * 2^LUX_SCALE
_M4T = 0x03fe   # 0.0624 * 2^LUX_SCALE
_K5T = 0x0138   # 0.61 * 2^RATIO_SCALE
_B5T = 0x016f   # 0.0224 * 2^LUX_SCALE
_M5T = 0x01fc   # 0.0310 * 2^LUX_SCALE
_K6T = 0x019a   # 0.80 * 2^RATIO_SCALE
_B6T = 0x00d2   # 0.0128 * 2^LUX_SCALE
_M6T = 0x00fb   # 0.0153 * 2^LUX_SCALE
_K7T = 0x029a   # 1.3 * 2^RATIO_SCALE
_B7T = 0x0018   # 0.00146 * 2^LUX_SCALE
_M7T = 0x0012   # 0.00112 * 2^LUX_SCALE
_K8T = 0x029a   # 1.3 * 2^RATIO_SCALE
_B8T = 0x0000   # 0.000 * 2^LUX_SCALE
_M8T = 0x0000   # 0.000 * 2^LUX_SCALE

_K1C = 0x0043   # 0.130 * 2^RATIO_SCALE
_B1C = 0x0204   # 0.0315 * 2^LUX_SCALE
_M1C = 0x01ad   # 0.0262 * 2^LUX_SCALE
_K2C = 0x0085   # 0.260 * 2^RATIO_SCALE
_B2C = 0x0228   # 0.0337 * 2^LUX_SCALE
_M2C = 0x02c1   # 0.0430 * 2^LUX_SCALE
_K3C = 0x00c8   # 0.390 * 2^RATIO_SCALE
_B3C = 0x0253   # 0.0363 * 2^LUX_SCALE
_M3C = 0x0363   # 0.0529 * 2^LUX_SCALE
_K4C = 0x010a   # 0.520 * 2^RATIO_SCALE
_B4C = 0x0282   # 0.0392 * 2^LUX_SCALE
_M4C = 0x03df   # 0.0605 * 2^LUX_SCALE
_K5C = 0x014d   # 0.65 * 2^RATIO_SCALE
_B5C = 0x0177   # 0.0229 * 2^LUX_SCALE
_M5C = 0x01dd   # 0.0291 * 2^LUX_SCALE
_K6C = 0x019a   # 0.80 * 2^RATIO_SCALE
_B6C = 0x0101   # 0.0157 * 2^LUX_SCALE
_M6C = 0x0127   # 0.0180 * 2^LUX_SCALE
_K7C = 0x029a   # 1.3 * 2^RATIO_SCALE
_B7C = 0x0037   # 0.00338 * 2^LUX_SCALE
_M7C = 0x002b   # 0.00260 * 2^LUX_SCALE
_K8C = 0x029a   # 1.3 * 2^RATIO_SCALE
_B8C = 0x0000   # 0.000 * 2^LUX_SCALE
_M8C = 0x0000   # 0.000 * 2^LUX_SCALE

class GroveDigitalLightSensor:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        
        self._ch0 = 0
        self._ch1 = 0
        self._ch0_low = 0
        self._ch0_high = 0
        self._ch1_low = 0
        self._ch1_high = 0
        
        self._power_up()
        self._write_register(_TSL2561_TIMING, 0x00)
        self._write_register(_TSL2561_INTRRUPT, 0x00)
        self._power_down()

    def _power_up(self):
        self._write_register(_TSL2561_CONTROL, 0x03)
        sleep(20)
        
    def _power_down(self):
        self._write_register(_TSL2561_CONTROL, 0x00)
        
    def _write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))

    def _read_register(self, address):        
        i2c.write(self._device_address, bytearray([address]))
        data = i2c.read(_DEFAULT_ADDRESS, 1)
        
        return data[0]
        
    def _read_bytes(self, address, num_bytes):
        i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)
        
    def _load_lux(self):
        data = self._read_bytes(_TSL2561_CHANNAL_0L, 2)
        data = unp('<H', data)[0]
        self._ch0_low = data
        
        data = self._read_bytes(_TSL2561_CHANNAL_0H, 2)
        data = unp('<H', data)[0]
        self._ch0_high = data
        
        data = self._read_bytes(_TSL2561_CHANNAL_1L, 2)
        data = unp('<H', data)[0]
        self._ch1_low = data

        data = self._read_bytes(_TSL2561_CHANNAL_1H, 2)
        data = unp('<H', data)[0]
        self._ch1_high = data

        self._ch0 = (self._ch0_high << 8) | self._ch0_low
        self._ch1 = (self._ch1_high << 8) | self._ch1_low

    def _calculate_lux(self, i_gain, t_int, i_type):
        ch_scale = (1 << _CH_SCALE)
        if t_int == 0:
             ch_scale = _CH_SCALE_TINT0
        if t_int == 1:
             ch_scale = _CH_SCALE_TINT1

        if not i_gain:
            ch_scale <<= 4
        
        channel0 = (self._ch0 * ch_scale) >> _CH_SCALE
        channel1 = (self._ch1 * ch_scale) >> _CH_SCALE

        ratio1 = 0
        if channel0 != 0:
            ratio1 = (channel1 << (_RATIO_SCALE + 1)) / channel0
        
        ratio = round(ratio1)
        
        if i_type == 0:
            if ratio >= 0 and ratio <= _K1T:
                b = _B1T
                m = _M1T
            elif ratio <= _K2T:
                b = _B2T
                m = _M2T
            elif ratio <= _K3T:
                b = _B3T
                m = _M3T
            elif ratio <= _K4T:
                b = _B4T
                m = _M4T
            elif ratio <= _K5T:
                b = _B5T
                m = _M5T
            elif ratio <= _K6T:
                b = _B6T
                m = _M6T
            elif ratio <= _K7T:
                b = _B7T
                m = _M7T
            elif ratio > _K8T:
                b = _B8T
                m = _M8T
            
        if i_type == 1:
            if ratio >= 0 and ratio <= _K1C:
                b = _B1C
                m = _M1C
            elif ratio <= _K2C:
                b = _B2C
                m = _M2C
            elif ratio <= _K3C:
                b = _B3C
                m = _M3C
            elif ratio <= _K4C:
                b = _B4C
                m = _M4C
            elif ratio <= _K5C:
                b = _B5C
                m = _M5C
            elif ratio <= _K6C:
                b = _B6C
                m = _M6C
            elif ratio <= K7C:
                b = _B7C
                m = _M7C
        
        temp = ((channel0 * b) - (channel1 * m))
        if temp < 0:
            temp = 0
            
        temp += (1 << (_LUX_SCALE - 1))
        lux = temp >> _LUX_SCALE
        
        return lux
    
    def dump_variables(self):
        print("ch0_low: {}".format(str(hex(self._ch0_low))))
        print("ch0_high: {}".format(str(hex(self._ch0_high))))
        print("ch1_low: {}".format(str(hex(self._ch1_low))))
        print("ch1_high: {}".format(str(hex(self._ch1_high))))
        print("ch0: {}".format(str(hex(self._ch0))))
        print("ch1: {}".format(str(hex(self._ch1))))
        
    def get_visible_lux(self):
        self._power_up()
        sleep(14)
        self._load_lux()
        self._power_down()
        
        if self._ch1 == 0:
            return 0
        
        if (self._ch0 / self._ch1 < 2) and (self._ch0 > 4900):
            return -1
        
        return self._calculate_lux(0, 0, 0)
         
    def get_ir_luminosity(self):
        self._power_up()
        sleep(14)
        self._load_lux()
        self._power_down()

        if self._ch1 == 0:
            return 0
        
        if (self._ch0 / self._ch1 < 2) and self._ch0 > 4900:
            return -1 # self._ch0 out of range, but self._ch1 not, the lux is not valid in this situation.
    
        return self._ch1

    def get_full_spectrum_luminosity(self):
        self._power_up()
        sleep(14)
        self._load_lux()
        self._power_down()
        
        if self._ch1 == 0:
            return 0;
    
        if (self._ch0 / self._ch1 < 2) and self._ch0 > 4900:
            return -1;  # self._ch0 out of range, but self._ch1 not, the lux is not valid in this situation.
    
        return self._ch0

def demo():
    i2c.init()
    
    sensor = GroveDigitalLightSensor()
    print("Visible Lux: {}".format(str(sensor.get_visible_lux())))
    print("IR Luminosity: {}".format(str(sensor.get_ir_luminosity())))
    print("Full Spectrum Luminosity: {}".format(str(sensor.get_full_spectrum_luminosity())))
    
#     print('')
#     sensor.dump_variables()
    
if __name__ == '__main__':
    demo()


