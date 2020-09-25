from genie import abstract
from genie.testbed import load
from genie.conf.base import device , Interface
from genie_modules import GenieClient
import concurrent.futures
from datetime import datetime
import pprint

def get_testbed():
    tb = input('Enter the full path to the testbed yaml file: ')
    load_tb = load(tb.strip())

    return load_tb

def update_interface_desc(devices,cdp):
    """Updates device interface desc with the cdp information from the get_cdp function
    """

    interface_dict = cdp
    management_interface = ['GigabitEthernet0/0','MgmtEth0/RP0/CPU0/0','GigabitEthernet0','mgmt0']

    # def updatter(devices):
    #     """Internal func to be called by pcall"""

    for device in devices:

        for index in interface_dict[device]["index"]: # For each cdp entry in each of the devices
            local_interface = interface_dict[device]["index"][index]["local_interface"]
            #pprint.pprint(local_interface)
            remote_device_hostname = interface_dict[device]["index"][index]["device_id"]
            remote_device_interface = interface_dict[device]["index"][index]["port_id"]
              
            if local_interface in management_interface: #Check if the local interface is on a BB Device
                interface_desc=(f'Conneted to backbone device {remote_device_hostname} via its {remote_device_interface} interface') # management interface, if so set this desc
                
            else: #Set the desc based on hostname and remote interface
                interface_desc=(f"Connected to {remote_device_hostname} via its {remote_device_interface} interface")           
            
            interface_obj = Interface(device=devices[device], name=local_interface)
            interface_obj.description = interface_desc

            final_config = interface_obj.build_config(apply=True)
            #print(f"Interface configuration for {device} \n {final_config}")

        #pcall_task = pcall(updatter,devices=self.devices.values())

def main():
    startTime = datetime.now()

    tb = get_testbed()
    client = GenieClient(tb,log=True)

    update_interface_desc(client.devices,client.get_cdp())

    total_time = (datetime.now() - startTime)
    print('Script took {} to complete'.format(total_time))

main()
