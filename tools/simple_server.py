from flask import Flask, flash, request, send_from_directory, redirect, url_for, jsonify
import requests

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
    URL = request.url
    METHOD = request.method
    print(cache)
    if URL not in cache:
        cache[URL] = resolve_request(URL, METHOD, request.data)
    else:
        print("returned a store response")
    return cache[URL]

def resolve_request(URL, method, req):
    """ Attempts to resolve a request using path """
    if method == "GET":
        r = requests.get(URL).content
    return r   

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
