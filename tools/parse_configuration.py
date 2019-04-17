import configparser
import sys
import json
import proxy_database as pr_db
from pathlib import Path
from flask import Response, jsonify

CONFIGURE_FILE = "./config"
TIME_DELTA = {"days": 86400000, "hours": 3600000, "minutes": 60000, "seconds": 1000, "milliseconds": 1}

class Configurations:
    def __init__(self):
        self.port_number = None
        self.custom_response_file = None
        #self.persistence = None
        self.allowable_urls = None
        self.timeout = None
        self.store = None
        self.retrieve = None

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
    
    if config['CUSTOM_RESPONSES']['use_custom_responses'] == "True":
        evaluate_custom_responses_parameters(config['CUSTOM_RESPONSES']['file_name'], user_params)
        
    return user_params

def evaluate_default_parameters(key, string, user_params):
    """ Converts from user-defined strings to parameters """
    if key == "port_number":
        user_params.port_number = int(string)
    elif key == "custom_response_file":
        user_params.custom_response_file = string
    elif key == "persistence":
        if string == "True":
            user_params.store = pr_db.store
            user_params.retrieve = pr_db.retrieve
        else:
            user_params.store = pr_db.temp_store
            user_params.retrieve = pr_db.temp_retrieve
    elif key == "allowable_urls":
        user_params.allowable_urls = string.split(' ')

def evaluate_custom_responses_parameters(file_name, user_params):
    ''' stores files from custom responses file'''
    custom_responses_file = Path(file_name)
    if not custom_responses_file.is_file():
        # if file does not already exist, create it with some example data
        example_data = {
            "method": "GET",
            "url": "http://httpbin.org/ip",
            "content": {
                "args": {},
                "headers": {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate",
                    "Host": "httpbin.org",
                    "User-Agent": "python-requests/2.21.0"
                },
                "origin": "140.233.185.118, 140.233.185.118",
                "url": "https://httpbin.org/ip"
            }
        }
        with open(file_name, 'x') as outfile:
            json.dump(example_data, outfile, indent=2)
    # read from file, format as response, store in database
    #return
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
        response = Response()
        response.content = json.dumps(data["content"])
        response.headers = data["content"]["headers"]
        user_params.store(data["method"], data["url"], response)


def initConfigureFile():
    """ Creates a configuration file with default parameters """
    config = configparser.ConfigParser()
    config.add_section('GENERAL') 
    config.set('GENERAL', 'port_number', '5000')
    config.set('GENERAL', 'persistence', 'True')
    config.set('GENERAL', 'allowable_urls', 'yourmom.com yourdad.com')
    config.add_section('CUSTOM_RESPONSES')
    config.set('CUSTOM_RESPONSES', 'use_custom_responses', 'True')
    config.set('CUSTOM_RESPONSES', 'file_name', 'custom_responses.json')
    config.add_section('TIMEOUT')
    config.set('TIMEOUT', 'days', '0')
    config.set('TIMEOUT', 'hours', '0')
    config.set('TIMEOUT', 'minutes', '0')
    config.set('TIMEOUT', 'seconds', '5')
    config.set('TIMEOUT', 'milliseconds', '0')
    with open(CONFIGURE_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()
