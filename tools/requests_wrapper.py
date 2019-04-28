import requests
from requests.models import Response
import sys
import proxy_database as pr_db
import parse_configuration
from datetime import datetime

class RequestsWrapper():
    def __init__(self):
        self.user_params = parse_configuration.userConfiguration()

    def __getattr__(self, name):
        """
        Handle method calls
        """

        known_methods = ["get", "post", "put", "delete", "patch"]
        
        def call_unknown_method(*args, **kwargs):
            try:
                method_to_call = getattr(requests, name)
                return method_to_call(*args, **kwargs)
            except:
                raise

        def call_known_method(*args, **kwargs):
            try:
                return self.handle_request(name, *args, **kwargs)
            except:
                raise
            
        
        if name in known_methods:
            return call_known_method
        else:
            return call_unknown_method

    def handle_request(self, method_name, *args, **kwargs):
        """
        If request is in database, return it. Otherwise, retrieve it normally,
        store it, then return it
        """

        response, timestamp = pr_db.retrieve(method_name.upper(), args[0])
        if response == None or self.invalid_timestamp(timestamp):
            # carry out request, store response database 
            response = self.resolve_request(method_name, *args, **kwargs)
        else:
            print("\t returned a store response")
        return self.format_response(response)
    
    def invalid_timestamp(self, timestamp):
        """
        Returns True if timestamp is invalid, or False otherwise
        """
        if timestamp == None:
            return True
        elif (timestamp + self.user_params.timeout) < pr_db.unix_time_millis(datetime.now()):
            return True
        else:
            return False

    def format_response(self, resp):
        """
        Correctly formats a request
        """
        # unsure if we need these, sometimes doesn't work without
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.headers.items()
                if name.lower() not in excluded_headers]

        # create and return Response object
        response = Response()
        response._content = resp.content
        response.status_code = resp.status_code
        response.headers = headers
        #response = Response(resp.content, resp.status_code, headers)
        return response

    def resolve_request(self, method_name, *args, **kwargs):
        """
        Resolves unstored responses
        """
        # get response from given request
        method_to_call = getattr(requests, method_name)
        resp = method_to_call(*args, **kwargs)
        print("\t resolving request")
        if any(api in args[0] for api in self.user_params.uncached_apis):
            return resp
        else:
            pr_db.store(method_name.upper(), args[0], resp)
            return resp
