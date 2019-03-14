from flask import Flask, flash, request, Response, send_from_directory, redirect, url_for, jsonify, json
import requests
import pickle

app = Flask(__name__)

cache = {}

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
    URL = request.url
    METHOD = request.method
    if (URL, METHOD) not in cache:
        # carry out request, store response in cache, update file cache
        cache[URL, METHOD] = test_resolve_request(request)
        update_cache()
    else:
        print("returned a store response")
    # return response from cache
    return cache[URL,METHOD]

def resolve_request(URL, method, req):
    """ Attempts to resolve a request using path """
    if method == "GET":
        r = requests.get(URL).content
    print()
    return r

def test_resolve_request(request):
    # get response from given request
    resp = requests.request(
        method=request.method,
        url=request.url,
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # unsure if we need these, sometimes doesn't work without
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # create and return Response object
    response = Response(resp.content, resp.status_code, headers)
    return response

def update_cache():
    # currently updating in a non-readable format, need to look into jsonifying
    # binary data
    pickle.dump(cache, open("save.p", "wb"))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
