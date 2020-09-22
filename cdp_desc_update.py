from genie import abstract
from genie.testbed import load
from genie.conf.base import device
from genie_modules import *
import concurrent.futures
from datetime import datetime
import pprint

def get_testbed():
    tb = input('Enter the full path to the testbed yaml file: ')
    load_tb = load(tb.strip())

    return load_tb

def main():
    startTime = datetime.now()

    tb = get_testbed()
    task = GenieClient(tb).update_interface_desc()

    #pprint.pprint(config_dict)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #         f1 = executor.map(GetConfig, tb)
    #         config_dict = GetConfig(tb).update_interface_desc()
    #         pprint.pprint(config_dict)

    total_time = (datetime.now() - startTime)
    print('Script took {} to complete'.format(total_time))


main()
