from genie import abstract
from genie.testbed import load
from genie.libs.conf.interface import Interface
from genie_modules import GenieClient
from pyats.async_ import pcall
from datetime import datetime
import pprint
import sys
import click 

def get_testbed(testbed):
    try:
        load_tb = load(testbed.strip())
        return load_tb

    except TypeError: #This should catch an invaild testbed file
        e = sys.exc_info()[1]
        print(e)
        sys.exit(1)   

def update_interface_desc(device):
    """Updates device interface desc with the cdp information 
    from the get_cdp function in the GenieClient
    """

    print(f'Running commands on {device}...')
    cdp_dict = device.parse("show cdp neighbors detail") #Get the cdp info on each call to the device
    
    management_interface = ['GigabitEthernet0/0','MgmtEth0/RP0/CPU0/0','GigabitEthernet0','mgmt0']

    for index in cdp_dict["index"]: # For each cdp entry in the cdp_dict
        local_interface = cdp_dict["index"][index]["local_interface"]
        remote_device_hostname = cdp_dict["index"][index]["device_id"]
        remote_device_interface = cdp_dict["index"][index]["port_id"]

        if local_interface in management_interface: #Check if the local interface is on a BB Device
            interface_desc=(f'Conneted to backbone device {remote_device_hostname} via its {remote_device_interface} interface') # management interface, if so set this desc
            
        else: #Set the desc based on hostname and remote interface
            interface_desc=(f"Connected to {remote_device_hostname} via its {remote_device_interface} interface")           
        
        #Here we create an inteface object so we can apply the desc string
        interface_obj = Interface(device=device, name=local_interface)
        interface_obj.description = interface_desc
        
        final_config = interface_obj.build_config(apply=True)
  
#click docs https://click.palletsprojects.com/en/7.x/#documentation
@click.command()
@click.option("--testbed","-t",type=str,help="Full path to a pyATS testbed file")
@click.option("--log","-l",is_flag=True,default=False,show_default=True,help="Logs the Genie stdout when connecting to devices",)
def main(testbed,log):
    
    tb = get_testbed(testbed)
    client = GenieClient(tb,log=log)
    devices = client.devices
    
    startTime = datetime.now()
    pcall_task = pcall(update_interface_desc, device=devices.values())
    total_time = (datetime.now() - startTime)
   
    print('Script took {} to update the device\'s interfaces'.format(total_time))

if __name__ == "__main__": 
    main()