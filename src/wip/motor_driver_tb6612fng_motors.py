# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c

_DEFAULT_ADDRESS         = 0x14

_DRIVER_SET_ADDR         = 0x11

_DRIVER_BRAKE            = 0x00
_DRIVER_STOP             = 0x01
_DRIVER_STANDBY          = 0x04
_DRIVER_NOT_STANDBY      = 0x05

_MOTOR_CLOCKWISE         = 0x02
_MOTOR_COUNTER_CLOCKWISE = 0x03

_MOTOR_A                 = 0
_MOTOR_B                 = 1

class GroveMotorDriverTB6612FNGMotors:
    def __init__(self, device_address = _DEFAULT_ADDRESS):
        self._device_address = device_address
        self.standby()
        
    def standby(self):
        data = bytes((_DRIVER_STANDBY, 0))
        # print("Data = {}".format(str(data)))
        i2c.write(self._device_address, data)
    
    def active(self):
        data = bytes((_DRIVER_NOT_STANDBY, 0))
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
    
    def forward_motors(self, speed = 125):
        self.motor_a_forward(speed)
        self.motor_b_forward(speed)
    
    def reverse_motors(self, speed = 125):
        self.motor_a_reverse(speed)
        self.motor_b_reverse(speed)
    
    def left_motors(self, speed = 125):
        self.motor_a_forward(speed)
        self.motor_b_reverse(speed)
    
    def right_motors(self, speed = 125):
        self.motor_b_forward(speed)
        self.motor_a_reverse(speed)
        
    def stop_motors(self):
        self.motor_a_stop()
        self.motor_b_stop()
        
    def break_motors(self):
        self.motor_a_break()
        self.motor_b_break()
    
    def motor_a_forward(self, speed = 125):
        self._forward(_MOTOR_A, speed)
        
    def motor_a_reverse(self, speed = 125):
        self._reverse(_MOTOR_A, speed)
        
    def motor_a_stop(self):
        self._stop(_MOTOR_A)
        
    def motor_a_break(self):
        self._break(_MOTOR_A)
        
    def motor_b_forward(self, speed = 125):
        self._forward(_MOTOR_B, speed)
        
    def motor_b_reverse(self, speed = 125):
        self._reverse(_MOTOR_B, speed)
        
    def motor_b_stop(self):
        self._stop(_MOTOR_B)
        
    def motor_b_break(self):
        self._break(_MOTOR_B)
        
    def _forward(self, motor, speed):
        if speed > 255:
            speed = 255
        elif speed < 1:
            speed = 1

        data = bytes((_MOTOR_CLOCKWISE, motor, speed))
        i2c.write(self._device_address, data)

    def _reverse(self, motor, speed):
        if speed > 255:
            speed = 255
        elif speed < 1:
            speed = 1
            
        data = bytes((_MOTOR_COUNTER_CLOCKWISE, motor, speed))
        i2c.write(self._device_address, data)
        
    def _stop(self, motor):
        data = bytes((_DRIVER_STOP, motor))
        i2c.write(self._device_address, data)
        
    def _break(self, motor):
        data = bytes((_DRIVER_BRAKE, motor))
        i2c.write(self._device_address, data)
        
def demo():
    motors = GroveMotorDriverTB6612FNGMotors()
    
    print("Motor A Forward, Speed 255")
    motors.motor_a_forward(255)
    sleep(5000)
    
    print("Motor A Breaking")
    motors.motor_a_break()
    sleep(1000)
    
    print("Motor A Reversing, Speed 100")
    motors.motor_a_reverse(100)
    sleep(5000)
    
    print("Motor A Stopping")
    motors.motor_a_stop()
    sleep(1000)
    
    print("Motor B Forward, Speed 255")
    motors.motor_b_forward(255)
    sleep(5000)
    
    print("Motor B Breaking")
    motors.motor_b_break()
    sleep(1000)
    
    print("Motor B Reversing, Speed 100")
    motors.motor_b_reverse(100)
    sleep(5000)
    
    print("Motor B Stopping")
    motors.motor_b_stop()
    sleep(1000)
    
    print("Motors forward")
    motors.forward_motors(255)
    sleep(5000)
    
    print("Motors stopping")
    motors.stop_motors()
    sleep(1000)
    
    print("Motors reversing")
    motors.reverse_motors(100)
    sleep(5000)
    
    print("Motors breaking")
    motors.break_motors()
    sleep(1000)
    
    print("Motors left")
    motors.left_motors(100)
    sleep(5000)
    motors.stop_motors()
    
    print("Motors right")
    motors.right_motors(100)
    sleep(5000)
    motors.stop_motors()
    
    print("")
    print("Demo ended")

if __name__ == '__main__':
    demo()
