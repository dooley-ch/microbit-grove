# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------
# NOTE: This example uses the ZS-042 PCB attached to the BBC micro via a Grove extension
#       cable over the I2C port

from microbit import i2c

_DEFAULT_ADDRESS = 0x68

_REG_SECOND      = 0
_REG_MINUTE      = 1
_REG_HOUR        = 2
_REG_WEEKDAY     = 3
_REG_DAY         = 4
_REG_MONTH       = 5
_REG_YEAR        = 6
_REG_CTRL        = 7
_REG_RAM         = 8

_MONDAY          = 1
_TUESDAY         = 2
_WEDNESDAY       = 3
_THURSDAY        = 4
_FRIDAY          = 5
_SATURDAY        = 6
_SUNDAY          = 7

i2c.init()

class RealTimeClock:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        self._second = None
        self._minute = None
        self._hour = None
        self._day_of_week = None
        self._day = None
        self._month = None
        self._year = None

    def	_write_register(self, address, data):
        i2c.write(self._device_address, bytearray([address, data]))

    def	_read_register(self, address):
        i2c.write(self._device_address, bytearray([address]))
        data =	i2c.read(_DEFAULT_ADDRESS, 1)
        
        return data[0]

    def start_clock(self):
        data = self._read_register(_REG_SECOND)
        
        # Save actual seconds and AND sec with bit 7 (sart/stop bit) = clock started
        self._write_register(_REG_SECOND, data & 0x7F)

    def stop_clock(self):
        data = self._read_register(_REG_SECOND)
        
        # Write seconds back and stop the clock
        self._write_register(_REG_SECOND, data | 0x80)

    def _dec_2_hex(self, dat):
        return (dat//10) * 16 + (dat%10)

    def _hex_2_dec(self, dat):
        return (dat//16) * 10 + (dat%16)

    def read_device(self):
        i2c.write(_DEFAULT_ADDRESS, bytearray([0]))
        data = i2c.read(_DEFAULT_ADDRESS, 7)

        self._second = self._hex_2_dec(data[0])
        self._minute = self._hex_2_dec(data[1])
        self._hour = self._hex_2_dec(data[2])
        self._day_of_week = self._hex_2_dec(data[3])
        self._day = self._hex_2_dec(data[4])
        self._month = self._hex_2_dec(data[5])
        self._year = self._hex_2_dec(data[6]) + 2000
      
    def write_device(self):
        data = bytearray(8)
        
        data[0] = 0
        data[1] = self._dec_2_hex(self._second % 60)
        data[2] = self._dec_2_hex(self._minute % 60)
        data[3] = self._dec_2_hex(self._hour % 24)
        data[4] = self._dec_2_hex(self._day_of_week % 8)
        data[5] = self._dec_2_hex(self._day % 32)
        data[6] = self._dec_2_hex(self._month % 13)
        data[7] = self._dec_2_hex(self._year % 100)
        
        i2c.write(_DEFAULT_ADDRESS, data) 
    
    def get_second(self):
        if self._second == None:
            self.read_device()
            
        return self._second
    
    def get_minute(self):
        if self._minute == None:
            self.read_device()
            
        return self._minute
    
    def get_hour(self):
        if self._hour == None:
            self.read_device()
            
        return self._hour
    
    def get_day_of_week(self):
        if self._day_of_week == None:
            self.read_device()
            
        return self._day_of_week
    
    def get_day_of_week_string(self):
        if self._day_of_week == None:
            self.read_device()
        
        if self._day_of_week == _MONDAY:
            return 'Mon'
        
        if self._day_of_week == _TUESDAY:
            return 'Tue'
        
        if self._day_of_week == _WEDNESDAY:
            return 'Wed'
        
        if self._day_of_week == _THURSDAY:
            return 'Thu'
        
        if self._day_of_week == _FRIDAY:
            return 'Fri'
        
        if self._day_of_week == _SATURDAY:
            return 'Sat'
        
        if self._day_of_week == _SUNDAY:
            return 'Sun'
            
        return None
    
    def get_day(self):
        if self._day == None:
            self.read_device()
            
        return self._day
    
    def get_month(self):
        if self._month == None:
            self.read_device()

        return self._month
    
    def get_year(self):
        if self._month == None:
            self.read_device()

        return self._year
      
    def get_date(self):
        return [self.get_year(), self.get_month(), self.get_day()]
    
    def get_time(self):
        return [self.get_hour(), self.get_minute(), self.get_second()]
    
    def fill_by_hms(self, hour, minute, second):
        if (self._year == None) or (self._month == None) or (self._day == None):
            raise IllegalArgumentError('Date must be set before time')
        
        self._second = second
        self._minute = minute
        self._hour = hour
    
    def fill_by_ymd(self, year, month, day):
        self._day = day
        self._month = month
        self._year = year
        
        if self._hour == None:
            self._hour = 12
        if self._minute == None:
            self._minute = 30
        if self._second == None:
            self._second = 30
        
    def fill_day_of_week(self, dow):
        if (self._year == None) or (self._month == None) or (self._day == None):
            raise IllegalArgumentError('Date must be set before day of the week')
        
        self._day_of_week = dow
    
    def DateTime(self, DT=None):
        if DT == None:
            i2c.write(_DEFAULT_ADDRESS, bytearray([0]))
            buf = i2c.read(_DEFAULT_ADDRESS, 7)
            DT = [0] * 8
            DT[0] = self._hex_2_dec(buf[6]) + 2000
            DT[1] = self._hex_2_dec(buf[5])
            DT[2] = self._hex_2_dec(buf[4])
            DT[3] = self._hex_2_dec(buf[3])
            DT[4] = self._hex_2_dec(buf[2])
            DT[5] = self._hex_2_dec(buf[1])
            DT[6] = self._hex_2_dec(buf[0])
            DT[7] = 0
            return DT
        else:
            buf = bytearray(8)
            buf[0] = 0
            buf[1] = self._dec_2_hex(DT[6]%60)    # second
            buf[2] = self._dec_2_hex(DT[5]%60)    # minute
            buf[3] = self._dec_2_hex(DT[4]%24)    # hour
            buf[4] = self._dec_2_hex(DT[3]%8)     # week day
            buf[5] = self._dec_2_hex(DT[2]%32)    # date
            buf[6] = self._dec_2_hex(DT[1]%13)    # month
            buf[7] = self._dec_2_hex(DT[0]%100)   # year
            i2c.write(_DEFAULT_ADDRESS, buf) 


def demo():
    rtc = RealTimeClock()
    rtc.read_device()
    
    print('Print current settings: ')
    print("\tYear: {}".format(str(rtc.get_year())))
    print("\tMonth: {}".format(str(rtc.get_month())))
    print("\tDay: {}".format(str(rtc.get_day())))
    print("\tDay Of Week: {}".format(rtc.get_day_of_week_string()))
    print('\tDate:', rtc.get_date())
    print('\tTime:', rtc.get_time())
    
    print('')
  
    print('Set the date and time to: 25-10-2021 17:32:05')
    rtc.fill_by_ymd(2021, 10, 25)
    rtc.fill_by_hms(17, 32, 5)
    rtc.fill_day_of_week(_MONDAY)
    rtc.write_device()

    print('')

    print('Print new settings: ')
    print("\tYear: {}".format(str(rtc.get_year())))
    print("\tMonth: {}".format(str(rtc.get_month())))
    print("\tDay: {}".format(str(rtc.get_day())))
    print("\tDay Of Week: {}".format(rtc.get_day_of_week_string()))
    print('\tDate:', rtc.get_date())
    print('\tTime:', rtc.get_time())
    
if __name__ == '__main__':
    demo()
