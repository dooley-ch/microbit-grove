# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import *

inA   = pin2
inB   = pin1

HIGH  = 1
LOW   = 0

def motor_off():
    inA.write_digital(LOW)
    inB.write_digital(LOW)

def motor_forward():
    inA.write_digital(HIGH)
    inB.write_digital(LOW)

def motor_reverse():
    inA.write_digital(LOW)
    inB.write_digital(HIGH)

def main():
    while True:
        a_pressed = button_a.was_pressed()
        b_pressed = button_b.was_pressed()
        
        if a_pressed and b_pressed:
            break
    
    motor_off()

if __name__ == '__main__':
    main()
