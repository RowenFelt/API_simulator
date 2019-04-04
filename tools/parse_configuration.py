import configparser
import sys
from pathlib import Path

class Configurations:
    def __init__(self):
        port_number = None
        response_file = None
        allowable_urls = None
        persistence = None

def userConfiguration():
    """ Initializes the configuration """ 
    configure_file = Path("./config")
    if configure_file.is_file():
        readConfigFile(configure_file)
    else:
        initConfigureFile(configure_file)

def readConfigFile(filepath):
    """ Reads a configuration file """
    config = configparser.ConfigParser()
    user_params = Configurations()

def initConfigureFile(filepath):
    """ Creates a configuration file with default parameters """
    config['DEFAULT'] = {'port_number': '5000',
                            'response_file': 'False',
                            'allowable_urls': 'None',
                            'persistence': 'True',
                            'response_timeout': '5:00'}
