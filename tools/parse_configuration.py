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
        self.uncached_apis = None
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

def dynamically_config(request_json, user_params):
    """ Configures user_parameters with the specified parameter, json body, and user params """
    for key in request_json.keys():
        if key == "TIMEOUT" or key == "timeout":
            user_params.timeout = 0
            for segment in request_json[key].keys():
                if segment in TIME_DELTA.keys():
                    user_params.timeout += TIME_DELTA[segment] * int(request_json[key][segment])
                else:
                    return None, False
        elif key == "persistence":
            if request_json[key] == "True" or request_json[key] == "true":
                user_params.persistence = True
            elif request_json[key] == "False" or request_json[key] == "false":
                user_params.persistence = False
            else:
                return None, False
        elif key == "response_file":
            if request_json[key] == "False" or request_json[key] == "false":
                user_params.response_file = False 
            else:
                user_params.response_file = request_json[key]
        elif key == "uncached_apis":
            user_params.uncached_apis.append(request_json[key])
        else:
            return None, False
    return user_params, True

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
    elif key == "uncached_apis":
        user_params.uncached_apis = string.split(' ')

def initConfigureFile():
    """ Creates a configuration file with default parameters """
    config = configparser.ConfigParser()
    config.add_section('GENERAL') 
    config.set('GENERAL', 'port_number', '5000')
    config.set('GENERAL', 'response_file', 'False')
    config.set('GENERAL', 'persistence', 'True')
    config.set('GENERAL', 'uncached_apis', 'yourmom.com http://httpbin.org/image/jpeg')
    config.add_section('TIMEOUT')
    config.set('TIMEOUT', 'days', '0')
    config.set('TIMEOUT', 'hours', '0')
    config.set('TIMEOUT', 'minutes', '0')
    config.set('TIMEOUT', 'seconds', '5')
    config.set('TIMEOUT', 'milliseconds', '0')
    with open(CONFIGURE_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()
