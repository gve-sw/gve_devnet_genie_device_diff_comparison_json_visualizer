# gve_devnet_geanie_device_diff_comparison_json_visualizer
prototype code that compares set of command configurations across a set of devices to a golden device. Additional script to help convert json data into a tree visualization

## Contacts
* Jorge Banegas

## Solution Components
* Geanie/PyATS
* Cisco CML
* NXOS devices
* Graphviz

## Installation/Configuration

(optional) This first step is optional if the user wants to leverage a virtual environment to install python packages

```shell
pip install virtualenv
virtualenv env
source env/bin/activate
```

Install python dependencies 

```shell
pip install -r requirements.txt
```

Include the JSON files that you would like to genereate a visualization for inside the json_files folder

Generate a genie testbed with all the devices that the user is looking to compare, an example testbed is provided. Also, [pyats create testbed command](https://pubhub.devnetcloud.com/media/genie-docs/docs/cli/genie_create.html) can also be leverage to generate your own testbed

Enter configuration details that includes the hostname for the golden device and the list of commands to compare against. Worth noting that only commands from https://developer.cisco.com/docs/genie-docs/ OS: NXOS are the commands that the script can accept 
    ```
        golden_device = 'nxos9000-0'
        command_list = ['show ntp peers','show version']
    ```
  
## Usage

To launch the json visualizer script (this creates a tree structure-like visualization from json data):

    (env) $ python jsontoimage.py
   
The image results will appear inside the json_output folder.

To launch the diff script (this script performs diff comparison against the golden device with all other devices):

    (env) $ python diff.py

The results of the diffs will appear inside the json_diffs folder.

# Screenshots
Example of visualization for json 
    ```
      {"name":"John", "age":30, "car":"Mercedes"}
    ```

![/IMAGES/output_example.png](/IMAGES/output_example.png)

Example of diff output 
    ```
      {"show ntp peers.peer-add": [["x.x.x.y", {"isconfigured": {"True": {"address": "x.x.x.y", "type": "server", "isconfigured": true}}}]], 
       "show ntp peers.peer-remove": [["x.x.x.z", {"isconfigured": {"True": {"address": "x.x.x.z", "type": "server", "isconfigured": true}}}]], 
       "show version.platform.hardware.processor_board_id-change": ["111111", "222222"], 
       "show version.platform.hardware.device_name-change": ["nxos9000-0", "nxos9000-1"], 
       "show version.platform.kernel_uptime.seconds-change": [47, 41]}
    ```
### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
