import requests
import os
import proxy_database as pr_db

proxy_urls = {
  'http': 'http://localhost:5000'
}

def get_test():
    print("get:")
    r = requests.get('http://httpbin.org/get', proxies=proxy_urls)
    r2 = requests.get('http://httpbin.org/get')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def put_test():
    print("put:")
    r = requests.put('http://httpbin.org/put', data = {'key':'value'}, proxies=proxy_urls)
    r2 = requests.put('http://httpbin.org/put', data = {'key':'value'})
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def post_test():
    print("post:")
    r = requests.post('http://httpbin.org/post', data = {'key':'value'}, proxies=proxy_urls)
    r2 = requests.post('http://httpbin.org/post', data = {'key':'value'})
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def delete_test():
    print("delete:")
    r = requests.delete('http://httpbin.org/delete', proxies = proxy_urls)
    r2 = requests.delete('http://httpbin.org/delete')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def different_status_test():
    r = requests.get('http://httpbin.org/status/404', proxies = proxy_urls)
    r2 = requests.get('http://httpbin.org/status/404')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def uncached_url_test():
    print("uncached urls:")
    url = "http://httpbin.org/image/jpeg"
    r = requests.get(url, proxies = proxy_urls)
    r2 = requests.get(url)
    database_response = pr_db.retrieve("GET", url)
    if r.content == r2.content and database_response == (None, None):
        print("passed")
    else:
        print("failed")
    return 0

def set_dynamic_config_test():
    print("dynamic configuration:")
    url = "http://localhost:5000/config"
    r = requests.post(url, json = {'persistence':'False', 'response_file':'True'}, proxies=proxy_urls)
    if r.status_code == 200:
        print("passed")
    else:
        print("failed")

if __name__ == "__main__":
    db = "./data/proxy_database.db"
    get_test()
    put_test()
    post_test()
    delete_test()
    uncached_url_test()
    set_dynamic_config_test()
