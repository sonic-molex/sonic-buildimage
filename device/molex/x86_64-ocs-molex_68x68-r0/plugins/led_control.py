#!/usr/bin/env python3

"""
led_control.py

Platform-specific LED control plugin for SONiC
Molex OCS 68x68 Platform

This module provides LED control functionality by:
1. Mapping abstract states to concrete LED colors
2. Controlling physical LEDs via HalPlatformApi Thrift interface

Design follows component.py style - Thrift connection is handled automatically
"""

try:
    from sonic_led.led_control_base import LedControlBase
    from sonic_py_common.logger import Logger
    from HalPlatformApi import client as hal_client
    from HalPlatformApi.client import *
    import time
except ImportError as e:
    raise ImportError(str(e) + " - required module not found")


# Constants
SYSLOG_IDENTIFIER = "led_control"
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 1  # seconds


class LedControl(LedControlBase):
    """
    Platform-specific LED control class for Molex OCS platform
    
    Pure LED hardware control library (no business logic).
    Implements the SONiC standard LED control interface.
    
    Design reference: component.py
    """
    
    # State to LED color mapping (hardcoded as per SONiC convention)
    STATE_TO_COLOR = {
        'up': 'green',
        'down': 'red',
        'degraded': 'amber',
        'off': 'off'
    }

    def __init__(self):
        """
        Initialize LED control module
        
        - Initialize Thrift connection to HalPlatformApiServer
        - Set up logging
        """
        LedControlBase.__init__(self)
        
        # Initialize logger
        self.log = Logger(SYSLOG_IDENTIFIER)
        
        # Initialize HAL Thrift connection (same as chassis.py)
        if not Initialize():
            error_msg = "Failed to initialize Thrift connection to HalPlatformApiServer"
            self.log.log_error(error_msg)
            raise RuntimeError(error_msg)
        
        self.log.log_info("LED control initialized successfully")
    
    def _is_transport_open(self):
        """
        Check if Thrift transport is open using standard Thrift API
        
        This method checks the Thrift transport layer without any business logic side effects.
        Supports multiple Thrift client structures for compatibility.
        
        Returns:
            bool: True if transport is open, False otherwise
        """
        if hal_client.client is None:
            return False
        
        try:
            # Try standard Thrift client structure: client._iprot.trans.isOpen()
            if hasattr(hal_client.client, '_iprot') and \
               hasattr(hal_client.client._iprot, 'trans') and \
               hasattr(hal_client.client._iprot.trans, 'isOpen'):
                return hal_client.client._iprot.trans.isOpen()
            
            # Try alternative structure: client._oprot.trans.isOpen()
            if hasattr(hal_client.client, '_oprot') and \
               hasattr(hal_client.client._oprot, 'trans') and \
               hasattr(hal_client.client._oprot.trans, 'isOpen'):
                return hal_client.client._oprot.trans.isOpen()
            
            # If no transport attribute found, cannot determine (assume closed)
            self.log.log_debug("Cannot find transport.isOpen() in Thrift client structure")
            return False
            
        except Exception as e:
            self.log.log_debug("Transport check failed: {}".format(str(e)))
            return False
    
    def _ensure_connection(self):
        """
        Ensure Thrift connection is active, reconnect if necessary
        
        This handles the case where HalPlatformApiServer restarts
        (e.g., during syncd container restart) and the connection becomes stale.
        
        Strategy: Check Thrift transport layer status using isOpen() method
        
        Returns:
            bool: True if connection is active, False if reconnection failed
        """
        # Check if transport is open using Thrift standard API
        if self._is_transport_open():
            return True  # Connection is valid
        
        # Connection is closed or stale, need to reconnect
        if hal_client.client is not None:
            self.log.log_warning("Thrift connection is stale, reconnecting...")
            try:
                Destroy()
            except Exception:
                pass
        
        # Attempt to reconnect
        for attempt in range(1, MAX_RECONNECT_ATTEMPTS + 1):
            self.log.log_info("Reconnection attempt {}/{}".format(
                attempt, MAX_RECONNECT_ATTEMPTS))
            
            if Initialize():
                self.log.log_notice("Successfully reconnected to HalPlatformApiServer")
                return True
            
            if attempt < MAX_RECONNECT_ATTEMPTS:
                time.sleep(RECONNECT_DELAY)
        
        self.log.log_error("Failed to reconnect after {} attempts".format(
            MAX_RECONNECT_ATTEMPTS))
        return False

    def port_link_state_change(self, port, state):
        """
        Handle port link state change and update corresponding LED
        
        This is the standard SONiC interface called by ledd or other modules.
        
        Args:
            port (str): Logical port name (e.g., "Fan0", "system", "LineCard0")
                       Port name is passed directly as LED name (1:1 mapping)
            state (str): Abstract state (e.g., "up", "down", "degraded", "off")
        
        Returns:
            bool: True if LED was set successfully, False otherwise
        """
        color = self.STATE_TO_COLOR.get(state, 'amber')
        self.log.log_info("LED: port='{}' state='{}' -> color='{}'".format(port, state, color))
        
        try:
            # Ensure connection before operation
            if not self._ensure_connection():
                return False
            
            # Call Thrift API to set LED
            result = LedSetState(port, color)
            
            if result is None:
                # Connection failed
                self.log.log_error("LedSetState returned None, connection failed")
                return False
            
            return result  # Success or expected failure
            
        except Exception as e:
            self.log.log_error("LED control exception: {}".format(str(e)))
            return False

    def get_led_status(self, port):
        """
        Get current LED status (reserved for future use)
        
        Args:
            port (str): Logical port name
        
        Returns:
            str: Current LED color, or None if unavailable
        """
        # Reserved for future implementation using LedGetState() Thrift API
        return None