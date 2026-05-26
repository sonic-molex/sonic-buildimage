#!/usr/bin/env python

########################################################################
# molex
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Components' (e.g., BIOS, CPLD, FPGA, etc.) available in
# the platform
#
########################################################################

try:
    import json
    import os
    import re
    import shutil
    import subprocess
    import sys
    import tarfile
    import time
    import traceback
    from sonic_py_common import device_info
    from sonic_platform_base.component_base import ComponentBase
    from HalPlatformApi.client import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


COMPONENT_RESTART_WARM = 1
COMPONENT_RESTART_COLD = 2
RESULT_OK = 0

class Component(ComponentBase):
    """molex Platform-specific Component class"""

    def __init__(self, desc, type_config=None):

        ComponentBase.__init__(self)
        self.desc = desc
        self.name = desc['name']
        self.type_config = type_config or {}

        # Load configuration attributes if available
        self.upgrade_workflow_flag = self.type_config.get('upgrade_workflow_flag', [])
        self.install_time_max = self.type_config.get('install_time_max', 60)
        self.reset_time_max = self.type_config.get('reset_time_max', 20)

        # Track temporary upgrade file path
        self._temp_upgrade_file = None

    def get_name(self):
        """
        Retrieves the name of the component

        Returns:
            A string containing the name of the component
        """
        return self.name

    def get_description(self):
        """
        Retrieves the description of the component

        Returns:
            A string containing the description of the component
        """
        return self.desc['description']

    def get_firmware_version(self):
        """
        Retrieves the firmware version of the component

        Returns:
            A string containing the firmware version of the component
        """
        return ComponentGetFwVer(self.name)

    def get_available_firmware_version(self, image_path):
        """
        Retrieves the available firmware version of the component

        Note: the firmware version will be read from image

        Args:
            image_path: A string, path to firmware image

        Returns:
            A string containing the available firmware version of the component
        """
        return None

    def install_firmware(self, image_path):
        """
        Installs firmware to the component

        Args:
            image_path: A string, path to firmware image

        Returns:
            A boolean, True if install was successful, False if not
        """
        return False

    def update_firmware(self, image_path):
        """
        Updates firmware of the component

        This API performs firmware update: it assumes firmware installation and loading in a single call.
        In case platform component requires some extra steps (apart from calling Low Level Utility)
        to load the installed firmware (e.g, reboot, power cycle, etc.) - this will be done automatically by API

        Args:
            image_path: A string, path to firmware image

        Returns:
            Boolean False if image_path doesn't exist instead of throwing an exception error
            Nothing when the update is successful

        Raises:
            RuntimeError: update failed
        """
        return True

    def auto_update_firmware(self, image_path, boot_type):
        """
        Updates firmware of the component

        This API performs firmware update automatically based on boot_type: it assumes firmware installation
        and/or creating a loading task during the reboot, if needed, in a single call.
        In case platform component requires some extra steps (apart from calling Low Level Utility)
        to load the installed firmware (e.g, reboot, power cycle, etc.) - this will be done automatically during the reboot.
        The loading task will be created by API.

        Args:
            image_path: A string, path to firmware image
            boot_type: A string, reboot type following the upgrade
                         - none/fast/warm/cold

        Returns:
            Output: A return code
                return_code: An integer number, status of component firmware auto-update
                    - return code of a positive number indicates successful auto-update
                        - status_installed = 1
                        - status_updated = 2
                        - status_scheduled = 3
                    - return_code of a negative number indicates failed auto-update
                        - status_err_boot_type = -1
                        - status_err_image = -2
                        - status_err_unknown = -3

        Raises:
            RuntimeError: auto-update failure cause
        """
        return 1

    def upgrade_wait_until_ok(self, func, max_attempts=5, interval=1):
        """
        Calls the given function every `interval` seconds until it returns True,
        or until the maximum number of attempts is reached.

        Args:
            func: A function that returns a boolean.
            max_attempts: Maximum number of attempts before giving up.
            interval: Time (in seconds) to wait between attempts.

        Returns:
            True if the function returned True within the allowed attempts, False otherwise.
        """
        # If max_attempts <= 0, skip waiting and return True immediately
        if max_attempts <= 0:
            print(f"Max attempts is {max_attempts}, skipping wait and returning True")
            return True

        result = RESULT_OK
        for attempt in range(max_attempts):
            time.sleep(interval)
            result = func(self.name)
            #print(f"Attempt {attempt + 1}: Result1 = {result}")
            if result == RESULT_OK:
                print(f"Attempt {attempt + 1} success")
                return True

        print(f"Max attempt {max_attempts} failed: {result}")
        return False

    def _prepare_upgrade_file(self, image_path):
        """
        Copy firmware image to /var/platform for container access

        Args:
            image_path: A string, path to firmware image

        Returns:
            A string, path to the copied file in /var/platform, or None if failed
        """
        try:
            # Check if source file exists
            if not os.path.exists(image_path):
                print(f"Error: Source image file does not exist: {image_path}")
                return None

            # Generate unique temporary filename
            timestamp = int(time.time())
            filename = os.path.basename(image_path)
            temp_path = f"/var/platform/fw_upgrade_{self.name}_{timestamp}_{filename}"

            print(f"Copying {image_path} to {temp_path}")

            # Copy file to /var/platform (this directory is mounted to container)
            shutil.copy2(image_path, temp_path)

            # Verify copy succeeded
            if not os.path.exists(temp_path):
                print(f"Error: Failed to copy image to {temp_path}")
                return None

            print(f"File copied successfully, size: {os.path.getsize(temp_path)} bytes")

            # Store the temporary file path
            self._temp_upgrade_file = temp_path
            return temp_path

        except Exception as e:
            print(f"Error preparing upgrade file: {e}")
            traceback.print_exc()
            return None

    def _cleanup_upgrade_file(self):
        """
        Remove temporary upgrade file from /var/platform
        """
        if self._temp_upgrade_file and os.path.exists(self._temp_upgrade_file):
            try:
                print(f"Cleaning up temporary file: {self._temp_upgrade_file}")
                os.remove(self._temp_upgrade_file)
                print("Temporary file removed successfully")
            except Exception as e:
                print(f"Warning: Failed to remove temporary file {self._temp_upgrade_file}: {e}")
            finally:
                self._temp_upgrade_file = None

class ComponentGeneral(Component):
    """
    molex Component general class
    upgrade step: upgrade -> upgrade_waiting -> upgrade_reset -> upgrade_waiting
    """

    UPGRADE_TIMEOUT_MAX = 300  # seconds (default)
    RESET_TIMEOUT_MAX = 10     # seconds (default)

    def __init__(self, desc, type_config=None):

        Component.__init__(self, desc, type_config)

        # Load upgrade_time_max from type_config, or use class default
        if type_config and 'upgrade_time_max' in type_config:
            self.UPGRADE_TIMEOUT_MAX = type_config['upgrade_time_max']
        else:
            self.UPGRADE_TIMEOUT_MAX = ComponentGeneral.UPGRADE_TIMEOUT_MAX

        # Load reset_time_max from type_config, or use class default
        if type_config and 'reset_time_max' in type_config:
            self.RESET_TIMEOUT_MAX = type_config['reset_time_max']
        else:
            self.RESET_TIMEOUT_MAX = ComponentGeneral.RESET_TIMEOUT_MAX

    def install_firmware(self, image_path):
        """
        Installs firmware to the component

        Args:
            image_path: A string, path to firmware image

        Returns:
            A boolean, True if install was successful, False if not
        """
        try:
            # Prepare firmware file in /var/platform
            temp_path = self._prepare_upgrade_file(image_path)
            if not temp_path:
                print("Failed to prepare upgrade file.")
                return False

            print(f"Using firmware image path: {temp_path}")

            if not self.upgrade(temp_path):
                print("Step 'upgrade' failed.")
                return False

            if not self.upgrade_waiting():
                print("Step 'upgrade_waiting' failed.")
                return False

            print("Firmware installation completed successfully.")
            return True

        except Exception as e:
            print(f"Error during firmware installation: {e}")
            traceback.print_exc()
            return False

        finally:
            # Always cleanup temporary file
            self._cleanup_upgrade_file()

    def update_firmware(self, image_path):
        """
        Updates firmware of the component

        This API performs firmware update: it assumes firmware installation and loading in a single call.
        In case platform component requires some extra steps (apart from calling Low Level Utility)
        to load the installed firmware (e.g, reboot, power cycle, etc.) - this will be done automatically by API

        Args:
            image_path: A string, path to firmware image

        Returns:
            Boolean False if image_path doesn't exist instead of throwing an exception error
            Nothing when the update is successful

        Raises:
            RuntimeError: update failed
        """
        try:
            # Prepare firmware file in /var/platform
            temp_path = self._prepare_upgrade_file(image_path)
            if not temp_path:
                print("Failed to prepare upgrade file.")
                return False

            print(f"Using firmware image path: {temp_path}")

            if not self.upgrade(temp_path):
                print("Step 'upgrade' failed.")
                return False

            if not self.upgrade_waiting():
                print("Step 'upgrade_waiting' failed.")
                return False

            # Check if upgrade_switch is needed based on upgrade_workflow_flag[1]
            if len(self.upgrade_workflow_flag) > 1 and self.upgrade_workflow_flag[1]:
                if not self.upgrade_switch():
                    print("Step 'upgrade_switch' failed.")
                    return False

           # Check if upgrade_reset is needed based on upgrade_workflow_flag[2]
            if len(self.upgrade_workflow_flag) > 2 and self.upgrade_workflow_flag[2]:
                if not self.upgrade_reset():
                    print("Step 'upgrade_reset' failed.")
                    return False
                if not self.upgrade_reset_waiting():
                    print("Step 'upgrade_reset_waiting' failed.")
                    return False

                # Check if upgrade_commit is needed based on upgrade_workflow_flag[3]
            if len(self.upgrade_workflow_flag) > 3 and self.upgrade_workflow_flag[3]:
                if not self.upgrade_commit():
                    print("Step 'upgrade_commit' failed.")
                    return False

            print("Firmware update completed successfully.")
            return True

        except Exception as e:
            print(f"Error during firmware update: {e}")
            traceback.print_exc()
            return False

        finally:
            # Always cleanup temporary file
            self._cleanup_upgrade_file()

    def auto_update_firmware(self, image_path, boot_type):
        """
        Updates firmware of the component

        This API performs firmware update automatically based on boot_type: it assumes firmware installation
        and/or creating a loading task during the reboot, if needed, in a single call.
        In case platform component requires some extra steps (apart from calling Low Level Utility)
        to load the installed firmware (e.g, reboot, power cycle, etc.) - this will be done automatically during the reboot.
        The loading task will be created by API.

        Args:
            image_path: A string, path to firmware image
            boot_type: A string, reboot type following the upgrade
                         - none/fast/warm/cold

        Returns:
            Output: A return code
                return_code: An integer number, status of component firmware auto-update
                    - return code of a positive number indicates successful auto-update
                        - status_installed = 1
                        - status_updated = 2
                        - status_scheduled = 3
                    - return_code of a negative number indicates failed auto-update
                        - status_err_boot_type = -1
                        - status_err_image = -2
                        - status_err_unknown = -3

        Raises:
            RuntimeError: auto-update failure cause
        """

        if self.update_firmware(image_path):
           return 2
        return -3

    def upgrade(self, image_path):
        """
        Upgrades firmware to the component

        Args:
            image_path: A string, path to firmware image

        Returns:
            A boolean, True if upgrade was successful, False if not
        """
        result = True
        print("upgrade +++")
        result = (RESULT_OK == ComponentUpgrade(self.name, image_path))
        print(f"upgrade --- result: {result}")

        return result

    def upgrade_waiting(self):
        """
        Waits for the upgrade to complete

        Returns:
            A boolean, True if upgrade was successful, False if not
        """
        result = True
        print("upgrade_waiting +++")
        #result = self.upgrade_wait_until_ok(lambda s: False, self.UPGRADE_TIMEOUT_MAX)
        result = self.upgrade_wait_until_ok(ComponentGetUpgradeStatus, self.UPGRADE_TIMEOUT_MAX)
        print(f"upgrade_waiting --- result: {result}")

        return result

    def upgrade_reset_waiting(self):
        """
        Waits for the upgrade_reset to complete

        Returns:
            A boolean, True if upgrade_reset was successful, False if not
        """
        result = True
        print(f"upgrade_reset_waiting +++")
        #result = self.upgrade_wait_until_ok(lambda s: False, self.UPGRADE_TIMEOUT_MAX)
        result = self.upgrade_wait_until_ok(ComponentGetUpgradeStatus, self.RESET_TIMEOUT_MAX)
        print(f"upgrade_reset_waiting --- result: {result}")

        return result

    def upgrade_switch(self):
        """
        Waits for the upgrade to complete

        Returns:
            A boolean, True if upgrade was successful, False if not
        """
        result = True
        print("upgrade_switch +++")
        #result = (RESULT_OK == ComponentUpgradeSwitch(self.name))
        print(f"upgrade_switch --- result: {result}")
        return result

    def upgrade_reset(self):
        """
        Waits for the upgrade to complete

        Returns:
            A boolean, True if upgrade was successful, False if not
        """
        result = True
        print("upgrade_reset +++")
        result = (RESULT_OK == ComponentReset(self.name, COMPONENT_RESTART_WARM))
        print(f"upgrade_reset --- result: {result}")

        return result

    def upgrade_commit(self):
        """
        Waits for the upgrade to complete

        Returns:
            A boolean, True if upgrade was successful, False if not
        """
        result = True
        print(f"upgrade_commit +++")
        #result = ComponentUpgradeCommit(self.name)
        print(f"upgrade_commit --- result: {result}")
        return result



class ComponentLogic(ComponentGeneral):
    """molex Component Logic(CPLD/FPGA) class"""

    UPGRADE_TIMEOUT_MAX = 350  # seconds (default for Logic components)

    def __init__(self, desc, type_config=None):

        ComponentGeneral.__init__(self, desc, type_config)

        # Load upgrade_time_max from type_config, or use class default
        if type_config and 'upgrade_time_max' in type_config:
            self.UPGRADE_TIMEOUT_MAX = type_config['upgrade_time_max']
        else:
            self.UPGRADE_TIMEOUT_MAX = ComponentLogic.UPGRADE_TIMEOUT_MAX

    def auto_update_firmware(self, image_path, boot_type):
        """
        Updates firmware of the component

        This API performs firmware update automatically based on boot_type: it assumes firmware installation
        and/or creating a loading task during the reboot, if needed, in a single call.
        In case platform component requires some extra steps (apart from calling Low Level Utility)
        to load the installed firmware (e.g, reboot, power cycle, etc.) - this will be done automatically during the reboot.
        The loading task will be created by API.

        Args:
            image_path: A string, path to firmware image
            boot_type: A string, reboot type following the upgrade
                         - none/fast/warm/cold

        Returns:
            Output: A return code
                return_code: An integer number, status of component firmware auto-update
                    - return code of a positive number indicates successful auto-update
                        - status_installed = 1
                        - status_updated = 2
                        - status_scheduled = 3
                    - return_code of a negative number indicates failed auto-update
                        - status_err_boot_type = -1
                        - status_err_image = -2
                        - status_err_unknown = -3

        Raises:
            RuntimeError: auto-update failure cause
        """
        try:
            # Prepare firmware file in /var/platform
            temp_path = self._prepare_upgrade_file(image_path)
            if not temp_path:
                print("Failed to prepare upgrade file.")
                return -3

            print(f"Using firmware image path: {temp_path}")

            if not self.upgrade(temp_path):
                print("Step 'upgrade' failed.")
                return -3

            if not self.upgrade_waiting():
                print("Step 'upgrade_waiting' failed.")
                return -3

            # Reset CPLD/FPGA during reboot phase
            print(f"Reset {self.name} during reboot phase scheduled")

            return 3  # status_scheduled - reset will happen during reboot

        except Exception as e:
            print(f"Error during auto-update firmware: {e}")
            traceback.print_exc()
            return -3

        finally:
            # Always cleanup temporary file
            self._cleanup_upgrade_file()

class ComponentHelper:
    """Component Helper class"""

    @staticmethod
    def _load_config():
        """
        Load component upgrade configuration from JSON file

        Returns:
            dict: Configuration dictionary or None if failed
        """
        try:
            platform_path = device_info.get_path_to_platform_dir()
            # Get the platform name from device_info
            platform, hwsku = device_info.get_platform_and_hwsku()

            # Construct config file path
            #config_file = os.path.join('/usr/share/sonic/device', platform, hwsku, 'component_upgrade_config.json')
            config_file = os.path.join(
                '/usr/share/sonic/device',
                platform,
                'component_upgrade_config.json'
            )

            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    #print(f"Loaded component config from: {config_file}")
                    return config
            else:
                print(f"Config file not found: {config_file}")
        except Exception as e:
            print(f"Failed to load component config: {str(e)}")

        return None

    @staticmethod
    def _get_component_type(component_name, config):
        """
        Get component type from component_name_list in config

        Args:
            component_name: Component name to search
            config: Configuration dictionary

        Returns:
            str: Component type or None if not found
        """
        if not config or 'component_type_name_mapping' not in config:
            return None

        for mapping in config['component_type_name_mapping']:
            if 'component_name_list' in mapping and component_name in mapping['component_name_list']:
                return mapping.get('type')

        return None

    @staticmethod
    def _get_component_type_config(component_type, config):
        """
        Get complete component type configuration from component_type_list

        Args:
            component_type: Component type to search
            config: Configuration dictionary

        Returns:
            dict: Complete type configuration including component_class and other attributes,
                  or None if not found
        """
        if not config or 'component_type_list' not in config:
            return None

        return config['component_type_list'].get(component_type)

    @staticmethod
    def _get_class_by_name(class_name):
        """
        Dynamically get class object by class name from current module

        Args:
            class_name: Name of the class to retrieve

        Returns:
            class: Class object or None if not found
        """
        # Get the class from the current module using sys.modules
        current_module = sys.modules[__name__]
        cls = getattr(current_module, class_name, None)
        if cls is None:
            print(f"Class '{class_name}' not found in current module")
        return cls

    @staticmethod
    def create_component_instance(item):
        """
        Create a component instance based on the component name

        The process follows these steps:
        1. Load configuration from component_upgrade_config.json
        2. Find component type from component_type_name_mapping by component name
        3. Find component_class and other attributes from component_type_list by type
        4. If steps 2-3 fail, return default Component base class

        Args:
            item: Component descriptor dictionary with 'name' field

        Returns:
            Component: A component instance (ComponentGeneral, ComponentLogic, or Component)
        """
        component_name = item['name']

        # Short-circuit: treat ONIE and BIOS with the default base Component
        if component_name in ('ONIE', 'BIOS'):
            #print(f"Component '{component_name}' uses default handling; returning base Component")
            return Component(item, None)

        # Step 1: Load configuration
        config = ComponentHelper._load_config()

        if not config:
            print(f"No configuration loaded, using default Component class for '{component_name}'")
            return Component(item, None)

        #

        # Step 2: Get component type from component_name_list
        component_type = ComponentHelper._get_component_type(component_name, config)

        if not component_type:
            print(f"Component type not found for '{component_name}' in config, using default Component class")
            return Component(item, None)

        # Step 3: Get complete component type configuration
        type_config = ComponentHelper._get_component_type_config(component_type, config)

        if not type_config:
            print(f"Type configuration not found for '{component_type}', using default Component class")
            return Component(item, None)

        class_name = type_config.get('component_class')

        if not class_name:
            print(f"Component class name not found in type config for '{component_type}', using default Component class")
            return Component(item, None)

        # Dynamically get the class by name
        cls = ComponentHelper._get_class_by_name(class_name)

        if not cls:
            print(f"Component class '{class_name}' not found in module, using default Component class")
            return Component(item, None)

        # Step 4: Create instance with the found class and type configuration
        #print(f"Creating {class_name} instance for '{component_name}' (type: {component_type})")
        return cls(item, type_config)