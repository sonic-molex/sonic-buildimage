########################################################################
#
# OTN-molex-ila
#
# Abstract base class for implementing a platform-specific class with
# which to interact with a hardware watchdog module in SONiC
#
########################################################################
import syslog

try:
    from sonic_platform_base.watchdog_base import WatchdogBase
    from HalPlatformApi.client import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Watchdog(WatchdogBase):
    """
    OTN-molex-ila Platform-specific Watchdog class
    """

    def __init__(self):
        pass

    def arm(self, seconds):
        """
        Arm the hardware watchdog with a timeout of <seconds> seconds.
        If the watchdog is currently armed, calling this function will
        simply reset the timer to the provided value. If the underlying
        hardware does not support the value provided in <seconds>, this
        method should arm the watchdog with the *next greater* available
        value.

        Returns:
            An integer specifying the *actual* number of seconds the watchdog
            was armed with. On failure returns -1.
        """
        result = WatchDogArm(0, seconds)
        if result is None:
            return -1
        return result

    def disarm(self):
        """
        Disarm the hardware watchdog

        Returns:
            A boolean, True if watchdog is disarmed successfully, False if not
        """
        return WatchDogDisrm(0)

    def is_armed(self):
        """
        Retrieves the armed state of the hardware watchdog.

        Returns:
            A boolean, True if watchdog is armed, False if not
        """
        return WatchDogIsArmed(0)

    def get_remaining_time(self):
        """
        If the watchdog is armed, retrieve the number of seconds remaining on
        the watchdog timer

        Returns:
            An integer specifying the number of seconds remaining on thei
            watchdog timer. If the watchdog is not armed, returns -1.
        """
        # HalPlatformApi does not currently provide a way to get remaining time
        return -1
