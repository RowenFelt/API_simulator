import requests

proxy_urls = {
        "http://httpbin.org": "localhost:5000"
    }

proxy_urls_2 = {
  'http': 'http://localhost:5000'
}

def get_test():
  print("get:")
  r = requests.get('http://httpbin.org/get', proxies=proxy_urls_2)
  r2 = requests.get('http://httpbin.org/get')
  #print(" ")
  #print(r.content)
  #print(" ")
  #print(r2.content)
  if r.content == r2.content:
    print("passed")
  else:
    print("failed")
  return 0

def put_test():
  print("put:")
  r = requests.put('http://httpbin.org/put', data = {'key':'value'}, proxies=proxy_urls_2)
  r2 = requests.put('http://httpbin.org/put', data = {'key':'value'})
  if r.content == r2.content:
    print("passed")
  else:
    print("failed")
  return 0

def post_test():
  print("post:")
  r = requests.post('http://httpbin.org/post', data = {'key':'value'}, proxies=proxy_urls_2)
  r2 = requests.post('http://httpbin.org/post', data = {'key':'value'})
  if r.content == r2.content:
    print("passed")
  else:
    print("failed")
  return 0

def delete_test():
  print("delete:")
  r = requests.delete('http://httpbin.org/delete', proxies = proxy_urls_2)
  r2 = requests.delete('http://httpbin.org/delete')
  if r.content == r2.content:
    print("passed")
  else:
    print("failed")
  return 0

def different_status_test():
  r = requests.get('http://httpbin.org/status/404', proxies = proxy_urls_2)
  r2 = requests.get('http://httpbin.org/status/404')
  if r.content == r2.content:
    print("passed")
  else:
    print("failed")
  return 0

if __name__ == "__main__":
  get_test()
  put_test()
  post_test()
  delete_test()
