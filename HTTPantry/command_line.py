import httpantry
import sys

def main():
    if len(sys.argv) == 1:
        print("help")
    else:
        arg = sys.argv[1]

        if arg == 'server':
            httpantry.http_proxy_server.init_proxy_server()
        else:
            print("help")