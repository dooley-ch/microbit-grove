# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import *
from six_position_dip_switch import *

obj = SixPositionDipSwitch()

print('Device Name:', obj.get_name())
print('Device Id:', obj.get_device_id())
print('Device Address:', obj.get_device_address())
print('Firmware:', obj.get_version())
print()
print('Button one:', obj.isButtonOneOn())
print('Button two:', obj.isButtonTwoOn())
print('Button three:', obj.isButtonThreeOn())
print('Button four:', obj.isButtonFourOn())
print('Button five:', obj.isButtonFiveOn())
print('Button six:', obj.isButtonSixOn())
