import configparser
import sys
import json
from pathlib import Path

CONFIGURE_FILE = "./config"
TIME_DELTA = {"days": 86400000, "hours": 3600000, "minutes": 60000, "seconds": 1000, "milliseconds": 1}

class Configurations:
    def __init__(self):
        self.port_number = None
        self.response_file = None
        self.persistence = None
        self.allowable_urls = None
        self.timeout = None

def userConfiguration():
    """ Initializes the configuration """ 
    configure_file = Path(CONFIGURE_FILE)
    if not configure_file.is_file():
        initConfigureFile()
    user_params = readConfigFile()
    return user_params

def readConfigFile():
    """ Reads a configuration file """
    config = configparser.ConfigParser()
    user_params = Configurations()
    config.read(CONFIGURE_FILE)
    for key in config['GENERAL']:
        evaluate_default_parameters(key, config['GENERAL'][key], user_params)
    user_params.timeout = 0
    for key in config['TIMEOUT']:
        if key in TIME_DELTA: 
            user_params.timeout += TIME_DELTA[key] * int(config['TIMEOUT'][key])
    return user_params

def evaluate_default_parameters(key, string, user_params):
    """ Converts from user-defined strings to parameters """
    if key == "port_number":
        user_params.port_number = int(string)
    elif key == "response_file":
        user_params.response_file = string
    elif key == "persistence":
        if string == "True":
            user_params.persistence = True
        else:
            user_params.persistence = False
    elif key == "allowable_urls":
        user_params.allowable_urls = string.split(' ')

def initConfigureFile():
    """ Creates a configuration file with default parameters """
    config = configparser.ConfigParser()
    config.add_section('GENERAL') 
    config.set('GENERAL', 'port_number', '5000')
    config.set('GENERAL', 'response_file', 'False')
    config.set('GENERAL', 'persistence', 'True')
    config.set('GENERAL', 'allowable_urls', 'yourmom.com yourdad.com')
    config.add_section('TIMEOUT')
    config.set('TIMEOUT', 'days', '0')
    config.set('TIMEOUT', 'hours', '0')
    config.set('TIMEOUT', 'minutes', '0')
    config.set('TIMEOUT', 'seconds', '5')
    config.set('TIMEOUT', 'milliseconds', '0')
    with open(CONFIGURE_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()
