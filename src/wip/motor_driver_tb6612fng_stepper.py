# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c

MOTOR_MODE_FULL_STEP  = 0
MOTOR_MODE_WAVE_DRIVE = 1
MOTOR_MODE_HALF_STEP  = 2
MOTOR_MODE_MICRO_STEP = 3

_DEFAULT_ADDRESS      = 0x14

_DRIVER_SET_ADDR      = 0x11

_DRIVER_STANDBY       = 0x04
_DRIVER_ACTIVE        = 0x05

_DRIVER_RUN           = 0x06
_DRIVER_STOP          = 0x07
_DRIVER_KEEP_RUN      = 0x08

class GroveMotorDriverTB6612FNGStepper:
    def __init__(self, max_steps = 200, rpm = 120, device_address = _DEFAULT_ADDRESS):
        self._device_address = device_address
        self._rpm = rpm
        self._max_steps = max_steps
        self.standby()
        
    def standby(self):
        data = bytes((_DRIVER_STANDBY, 0))
        # print("Data = {}".format(str(data)))
        i2c.write(self._device_address, data)
    
    def active(self):
        data = bytes((_DRIVER_ACTIVE, 0))
        # print("Data = {}".format(str(data)))
        i2c.write(self._device_address, data)
    
    def stop(self):
        data = bytes((_DRIVER_STOP, 0))
        i2c.write(self._device_address, data)
        
    def move(self, steps, mode = MOTOR_MODE_MICRO_STEP):
        cw = 0

        if steps > 0:
            cw = 1
        elif steps == 0:
            self.stop()
            return
        elif steps == -self._max_steps:
            steps = self._max_steps
        else:
            steps = -steps
            
        if self._rpm < 1:
            self._rpm = 1
        elif self._rpm > 300:
            self._rpm = 300

        ms_per_step = 7000.0 / self._rpm

        data = bytes((_DRIVER_RUN, mode, int(cw), steps, int(steps >> 8), int(ms_per_step), (int(ms_per_step) >> 8)))
        
        # print("Data = {}".format(str(data)))
        i2c.write(self._device_address, data)
    
    def rotate(self, mode = MOTOR_MODE_FULL_STEP, forward = True):
        if forward:
            steps = self._max_steps
        else:
            steps = -self._max_steps
        
        self.move(steps, mode)

    def run(self, mode = MOTOR_MODE_MICRO_STEP, clockwise = True):
        cw = 5 if clockwise else 4
        
        if self._rpm < 1:
            self._rpm = 1
        elif self._rpm > 300:
            self._rpm = 300

        ms_per_step = 7000.0 / self._rpm
        
        data = bytes((_DRIVER_KEEP_RUN, int(mode), int(cw), int(ms_per_step), (int(ms_per_step) >> 8)))
        
        # print("Data = {}".format(str(data)))
        i2c.write(self._device_address, data)        
    
    def set_address(self, address):
        if address == 0x00:
            return
        if address == 0x80:
            return
        
        data = bytes((_DRIVER_SET_ADDR, address))
        i2c.write(self._device_address, data)
        self.device_address = address    
    
def demo():
    stepper = GroveMotorDriverTB6612FNGStepper()
    
    print("Moter in standby (energy saving)")
    stepper.standby()
    sleep(1000)
    
    print("Moving forward 200 steps...")
    stepper.move(200)
    sleep(2000)
    
    print("Moving backwards 200 steps...")
    stepper.move(-200)
    sleep(2000)
    
    print("Moving forward 100 steps...")
    stepper.move(100)
    sleep(2000)
    
    print("Moving backwards 100 steps...")
    stepper.move(-100)
    sleep(2000)
    
    print("Moving forward 25 steps...")
    stepper.move(25)
    sleep(2000)
    
    print("Moving backwards 75 steps...")
    stepper.move(-75)
    sleep(2000)
    
    print("Moving forward 190 steps...")
    stepper.move(190)
    sleep(2000)
    
    print("Moving backwards 190 steps...")
    stepper.move(-190)
    sleep(2000)
    
    print("Rotating...")
    stepper.rotate()
    sleep(2000)
    
    print("Run continuously...")
    stepper.run()
    sleep(10000)
    
    print("Stop motor...")
    stepper.stop()
    sleep(1000)
    stepper.standby()
    
    print("Step by step.....")
    max_steps = 0
    while True:
        if max_steps == 200:
            break
        stepper.move(5)
        sleep(1000)
        max_steps = max_steps + 5
        
    print("")
    print("Demo over")
    
if __name__ == '__main__':
    demo()


