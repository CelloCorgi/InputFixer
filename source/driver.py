"""
This file contains the main driver for the InputFixer tool

Run as such: Python3 driver.py config_file.json(optional)
If no configuration file is provided, the default is run, which you probably don't want
Config is in json format. See the readme for information on how to format the config file

"""

import sys
import json
from inFix_config import Config

def load_configuration(file_name):
    """
    This function loads the configuration as necessary
    """
    if len(sys.argv) < 3:
        print("No configuration file provided. Using default configuration")
        return Config()
    try:
        with open(file_name, 'r') as config_file:
            return Config(json.loads(next(config_file)))
    except:
        print("Unable to load provided config file. Terminating program execution.\n")
        sys.exit()

if __name__ == "__main__":

    # Load the configiration file
    inFix_config = load_configuration(sys.argv[-1])
    
