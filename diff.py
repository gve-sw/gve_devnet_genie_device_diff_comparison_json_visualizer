""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

# Import Genie
from unittest.util import _count_diff_hashable
from genie import testbed
import dictdiffer
import config
import json
import glob
import os
import pprint

ROOT_DIR = os.path.abspath(os.curdir)
DIFF_DIR = ROOT_DIR + '/json_diffs/'

# Loading testbed file for geanie
testbed = testbed.load('sandbox-testbed.yaml')

# golden device I want to connect to
golden_device = testbed.devices[config.golden_device]

# Connect to it
golden_device.connect()

# finding every other device from the testbed to compare configurations
for device in testbed.devices.keys():
    temp_dict_golden = {}
    temp_dict_device = {}

    for command in config.command_list:
        if device != config.golden_device:
            output_golden = golden_device.parse(command)
            temp_dict_golden[command] = output_golden

            target_device = testbed.devices[device]
            target_device.connect()

            output = target_device.parse(command)
            temp_dict_device[command] = output
        else:
            continue

    # naming the diff file by the hostname of the device
    filename =  DIFF_DIR + str(device) + "_output.json"

    # printing the output for the commands on the golden device
    pprint.pprint(temp_dict_golden)

    # printing the output for the commands on the selected device
    pprint.pprint(temp_dict_device)

    if device != config.golden_device:
        print(config.golden_device)
        print(device)

        output = {}
        for diff in list(dictdiffer.diff(temp_dict_golden, temp_dict_device)):
            temp_key = str(diff[1]) + '-' + str(diff[0])
            output[temp_key] = diff[2]      

        with open(filename, 'w') as f:
            json.dump(output, f)
