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
    tb = get_testbed()
    task = GenieClient(tb).get_running_config()

    pprint.pprint(task)

main()
