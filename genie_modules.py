from genie import abstract
from genie.conf.base import device
from genie.libs.conf.interface import Interface
from pyats.async_ import pcall
import pyats
import pprint

class GenieClient():
    """An Object to interact with pyATS's Genie parsers"""

    def __init__(self,testbed,log=False):
        """Init the Config Object and connect to Testbed"""

        self.testbed = testbed.connect(log_stdout=log)
        self.devices = testbed.devices

    def push_config(self):
        user_input = input('Do you want to push this config to the device? Y/N ')
        if user_input == 'y' or 'Y':
            push_config = True

        else:
            push_config = False

        return push_config

    def get_info(self,command):
        """Generic method to get strcutred
        data back. Depends on if the genie parser is present for that command
        """
        for device in self.devices:
            print(f'Running commands on {device}...')
            command = self.devices[device].parse(command)

        return command

    def get_running_config(self):
        """Grabs the running config from devices in the
        testbed file using genie"""

        device_configs = {}

        for device in self.devices:
            print(f'Running commands on {device}...')
            config = self.devices[device].parse('show running-config')
            device_configs[device] = config

        return device_configs


    def get_cdp(self,cdp_dict={}):
        """Gets CDP neighbors information and returns a dict
        with the key as the device name
        """
        for device in self.devices:
            print(f'Running commands on {device}...')
            cdp_dict[device] = self.devices[device].parse("show cdp neighbors detail")
            #pprint.pprint(cdp_dict,indent=4)

        return cdp_dict


    def get_inventory(self):
        """Get inventory from testbed devices"""
        inventory_dict = {}

        for device in self.devices:
            inventory_dict[device] = self.devices[device].parse('show inventory')

        return inventory_dict
