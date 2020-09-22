#from pyats.testbed import loader
from genie import abstract
from genie.testbed import load
from genie.conf.base import device
import pprint

tb = load('/home/mek/pyATS/yaml/N9504-Leaf-Spine-2.yaml')

config = []

for device in tb.devices:
    config = tb.devices[device].build_config(apply=False)
    #response = (tb.devices[device].build_config(apply=False))

# for device in tb.devices:
#     tb.devices[device].connect()
#     response.append(tb.devices[device].parse('show cdp neighbors'))
#     tb.devices[device].disconnect()

pprint.pprint(config)
