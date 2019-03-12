import requests

proxy_urls = {
        "http://httpbin.org": "localhost:5000"
    }

def main():
    r = requests.get("http://httpbin.org/ip", proxies=proxy_urls)
    print(r.status_code)
    print(r.json())
    return 0

if __name__ == "__main__":
    main()
