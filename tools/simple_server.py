from flask import Flask, flash, request, Response, send_from_directory, redirect, url_for, jsonify, json, make_response
import requests
import proxy_database as pr_db
import parse_configuration
from datetime import datetime

app = Flask(__name__)
user_params = None


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

#catch all URL
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(path):
    """ Returns a stored response if such exists, otherwise returns -1 """
    # get url and method to store in cache
    response, timestamp = pr_db.retrieve(request.method, request.url)
    if response == None or invalid_timestamp(timestamp):
        print(response)
        print(timestamp)
       # carry out request, store response database 
        response = resolve_request(request)
    else:
        print("returned a store response")
    return format_response(response)

@app.route('/config', methods=['POST'])
def config_dynamic():
    """ Sets a user configuration as described in the request body """
    global user_params
    temp_params, result = parse_configuration.dynamically_config(request.json, user_params)
    if result:
        user_params = temp_params
        print(user_params.persistence)
        print(user_params.response_file)
        return make_response("Success", 200)
    else:
        return make_response("Failure", 404)

def invalid_timestamp(timestamp):
    """ Returns True if timestamp is invalid, or False otherwise """
    if timestamp == None:
        return True
    elif (timestamp + user_params.timeout) < pr_db.unix_time_millis(datetime.now()):
        return True
    else:
        return False
    
def format_response(resp):
    ''' correctly formats a request '''
    # unsure if we need these, sometimes doesn't work without
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.headers.items()
               if name.lower() not in excluded_headers]

    # create and return Response object
    response = Response(resp.content, resp.status_code, headers)
    return response

def resolve_request(request):
    # get response from given request
    resp = requests.request(
        method=request.method,
        url=request.url,
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    print("resolving request")
    if any(api in request.url for api in user_params.uncached_apis):
        return resp
    else:
        pr_db.store(request.method, request.url, resp)
        return resp


def update_cache():
    # currently updating in a non-readable format, need to look into jsonifying
    # binary data
    pickle.dump(cache, open("save.p", "wb"))

if __name__ == "__main__":
    user_params = parse_configuration.userConfiguration()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(port=user_params.port_number)
