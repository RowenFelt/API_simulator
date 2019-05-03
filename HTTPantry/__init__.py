import httpantry.parse_configuration as parse_configuration
import requests
from .requests_wrapper import handle_request

print("httpantry imported")

user_params = parse_configuration.userConfiguration()

def __getattr__(name):
    """
    Handle method calls
    """

    print(name)

    known_methods = ["get", "post", "put", "delete", "patch"]
    
    def call_unknown_method(*args, **kwargs):
        try:
            method_to_call = getattr(requests, name)
            return method_to_call(*args, **kwargs)
        except:
            raise

    def call_known_method(*args, **kwargs):
        try:
            return handle_request(name, *args, **kwargs)
        except:
            raise
    
    if name in known_methods:
        return call_known_method
    else:
        return call_unknown_method