#!/usr/bin/env python

########################################################################
# OTN-molex-ila
#
# Minimal ThermalManager: sets all fan speeds to 50% at boot.
#
########################################################################

from sonic_platform_base.sonic_thermal_control.thermal_manager_base import ThermalManagerBase


class ThermalManager(ThermalManagerBase):

    @classmethod
    def load(cls, policy_file_name):
        """No policy file needed – skip loading."""
        pass

    @classmethod
    def init_thermal_algorithm(cls, chassis):
        """Set all fans to 50% at startup."""
        for fan in chassis.get_all_fans():
            print(f"Setting fan {fan.get_name()} to 50%")
            fan.set_speed(50)
