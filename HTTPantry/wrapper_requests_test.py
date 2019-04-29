import requests as req
import os
import proxy_database as pr_db
#from requests_wrapper import RequestsWrapper
import time

import TestLibrary as requests

def get_test():
    print("get:")
    r = requests.get('https://httpbin.org/get')
    r2 = req.get('https://httpbin.org/get')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def put_test():
    print("put:")
    r = requests.put('http://httpbin.org/put', data = {'key':'value'})
    r2 = req.put('http://httpbin.org/put', data = {'key':'value'})
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def post_test():
    print("post:")
    t1 = time.time()
    r = requests.post('http://httpbin.org/post', data = {'key':'value'})
    t2 = time.time()
    r2 = req.post('http://httpbin.org/post', data = {'key':'value'})
    t3 = time.time()
    if r.content == r2.content:
        print("passed")
        normal_time = t3-t2
        wrapper_time = t2-t1
        times_faster = normal_time/wrapper_time
        print("(",normal_time, wrapper_time, times_faster, "times faster)")
    else:
        print("failed")
    return 0

def delete_test():
    print("delete:")
    r = requests.delete('http://httpbin.org/delete')
    r2 = req.delete('http://httpbin.org/delete')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def different_status_test():
    r = requests.get('http://httpbin.org/status/404')
    r2 = req.get('http://httpbin.org/status/404')
    if r.content == r2.content:
        print("passed")
    else:
        print("failed")
    return 0

def uncached_url_test():
    print("uncached urls:")
    url = "http://httpbin.org/image/jpeg"
    r = requests.get(url)
    r2 = req.get(url)
    database_response = pr_db.retrieve("GET", url)
    if r.content == r2.content and database_response == (None, None):
        print("passed")
    else:
        print("failed")
    return 0

def set_dynamic_config_test():
    print("dynamic configuration:")
    url = "http://localhost:5000/config"
    r = requests.post(url, json = {'persistence':'False', 'response_file':'True'})
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
    #set_dynamic_config_test()
