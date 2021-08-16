# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import *
from grove_6_position_dip_switch import GroveSixPositionDipSwitch

display.clear()

dipSwitch = GroveSixPositionDipSwitch()

print('Device Name:', dipSwitch.get_name())
print('Device Id:', dipSwitch.get_device_id())
print('Device Address:', dipSwitch.get_device_address())
print('Firmware:', dipSwitch.get_version())


while True:
    if dipSwitch.has_changed():
        print()
        print('Button one:', dipSwitch.is_button_1_on())
        print('Button two:', dipSwitch.is_button_2_on())
        print('Button three:', dipSwitch.is_button_3_on())
        print('Button four:', dipSwitch.is_button_4_on())
        print('Button five:', dipSwitch.is_button_5_on())
        print('Button six:', dipSwitch.is_button_6_on())
        print()
        print('Value:', dipSwitch.get_value())
        