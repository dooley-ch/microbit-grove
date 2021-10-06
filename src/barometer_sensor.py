# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c, display, button_b
from ustruct import unpack as unp
from utime import ticks_diff, ticks_ms, sleep_ms

_DEFAULT_ADDRESS         = 0x77

_BMP280_REG_DIG_T1       = 0x88
_BMP280_REG_DIG_T2       = 0x8A
_BMP280_REG_DIG_T3       = 0x8C

_BMP280_REG_DIG_P1       = 0x8E
_BMP280_REG_DIG_P2       = 0x90
_BMP280_REG_DIG_P3       = 0x92
_BMP280_REG_DIG_P4       = 0x94
_BMP280_REG_DIG_P5       = 0x96
_BMP280_REG_DIG_P6       = 0x98
_BMP280_REG_DIG_P7       = 0x9A
_BMP280_REG_DIG_P8       = 0x9C
_BMP280_REG_DIG_P9       = 0x9E

_BMP280_REG_CHIPID       = 0xD0

_BMP280_REG_CONTROL      = 0xF4
_BMP280_REGISTER_DATA    = 0xF7

_BMP280_TEMP_OS_2        = 2
_BMP280_PRES_OS_16       = 5

class GroveBarometerSensor:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS

        assert self._read_register(_BMP280_REG_CHIPID, 1)[0] == 0x58, 'BMP280_REG_CHIPID is not equal to 0x58'
        
        self._last_read = 0
        
        self._temperature_fine = 0
        self._temperature_raw = 0
        self._temperature = 0
 
        self._pressure_raw = 0
        self._pressure = 0
        
        self._digit_t1 = unp('<H', self._read_register(_BMP280_REG_DIG_T1, 2))[0]
        self._digit_t2 = unp('<h', self._read_register(_BMP280_REG_DIG_T2, 2))[0]
        self._digit_t3 = unp('<h', self._read_register(_BMP280_REG_DIG_T3, 2))[0]
   
        self._digit_p1 = unp('<H', self._read_register(_BMP280_REG_DIG_P1, 2))[0]
        self._digit_p2 = unp('<h', self._read_register(_BMP280_REG_DIG_P2, 2))[0]
        self._digit_p3 = unp('<h', self._read_register(_BMP280_REG_DIG_P3, 2))[0]
        self._digit_p4 = unp('<h', self._read_register(_BMP280_REG_DIG_P4, 2))[0]
        self._digit_p5 = unp('<h', self._read_register(_BMP280_REG_DIG_P5, 2))[0]
        self._digit_p6 = unp('<h', self._read_register(_BMP280_REG_DIG_P6, 2))[0]
        self._digit_p7 = unp('<h', self._read_register(_BMP280_REG_DIG_P7, 2))[0]
        self._digit_p8 = unp('<h', self._read_register(_BMP280_REG_DIG_P8, 2))[0]
        self._digit_p9 = unp('<h', self._read_register(_BMP280_REG_DIG_P9, 2))[0]
   
        self._write_register(_BMP280_REG_CONTROL, 0x3F)
        
    def _write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))
    
    def _read_register(self, address, num_bytes):
        i2c.write(self._device_address, bytearray([address]))
        return i2c.read(_DEFAULT_ADDRESS, num_bytes)

    def _read_all_data(self):
        if ticks_diff(ticks_ms(), self._last_read) > 150:
            self._last_read = ticks_ms()
            
            self._write_register(_BMP280_REG_CONTROL, (_BMP280_TEMP_OS_2 + (_BMP280_PRES_OS_16 << 3) + (1 << 6)))
            sleep_ms(120)
            
            data = self._read_register(_BMP280_REGISTER_DATA, 6)
            
            self._pressure_raw = (data[0] << 12) + (data[1] << 4) + (data[2] >> 4)
            self._temperature_raw = (data[3] << 12) + (data[4] << 4) + (data[5] >> 4)
 
            self._temperature_fine = 0
            self._temperature = 0
            self._pressure = 0
            
    def _calculate_temperature(self):
        self._read_all_data()
        
        if self._temperature_fine == 0:
            var1 = (((self._temperature_raw >> 3) - (self._digit_t1 << 1)) * self._digit_t2) >> 11
            var2 = (((((self._temperature_raw >> 4) - self._digit_t1) * ((self._temperature_raw >> 4) - self._digit_t1)) >> 12) * self._digit_t3) >> 14
            self._temperature_fine = var1 + var2
            
        if self._temperature == 0:
            self._temperature = ((self._temperature_fine * 5 + 128) >> 8) / 100.
            
        return self._temperature
        
    def _calculate_pressure(self):
        self._calculate_temperature()

        if self._pressure == 0:
            var1 = self._temperature_fine - 128000
            var2 = var1 * var1 * self._digit_p6
            var2 = var2 + ((var1 * self._digit_p5) << 17)
            var2 = var2 + (self._digit_p4 << 35)
            var1 = ((var1 * var1 * self._digit_p3) >> 8) + ((var1 * self._digit_p2) << 12)
            var1 = (((1 << 47) + var1) * self._digit_p1) >> 33
 
            if var1 == 0:
                return 0
 
            p = 1048576 - self._pressure_raw
            p = int((((p << 31) - var2) * 3125) / var1)
            var1 = (self._digit_p9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self._digit_p8 * p) >> 19
 
            p = ((p + var1 + var2) >> 8) + (self._digit_p7 << 4)
            self._pressure = (p / 256.0) / 100
            
        return self._pressure
    
    def _calculate_altitude(self):
        a = self._calculate_pressure() / 101325
        b = 1 / 5.25588
        c = pow(a, b)
        c = c / 0.0000225577
        
        return c
    
    def get_temperature(self, fahrenheit = False):
        value = self._calculate_temperature()
        
        if fahrenheit:
            value = (value * 9/5) + 32
        
        return round(value)
    
    def get_pressure(self, imperial = False):
        value = self._calculate_pressure()
        
        if imperial:
            value /= 33.87
        
        return round(value)
    
    def get_altitude(self, imperial = False):
        value = self._calculate_altitude()
        
        if imperial:
            value /= 2.54
            value /= 12
        else:
            value /= 100
            
        return round(value)        
    
def demo():
    sensor = GroveBarometerSensor()
    
    display.clear()
    display.show('>')

    print('Altitude:', sensor.get_altitude())
    
    while True:
        if button_b.was_pressed():
            break
        
        print('Metric')
        print("\tTemperature: {}C".format(str(sensor.get_temperature())))
        print("\tPressure: {} mbar".format(str(sensor.get_pressure())))
        print("\tAltitude: {}M".format(str(sensor.get_altitude())))
        print('')
        print('Imperial')
        print("\tTemperature: {}F".format(str(sensor.get_temperature(True))))
        print("\tPressure: {} inHg".format(str(sensor.get_pressure(True))))
        print("\tAltitude: {} ft".format(str(sensor.get_altitude(True))))
        print('')
        
        sleep(3000)
        
if __name__ == '__main__':
    demo()
