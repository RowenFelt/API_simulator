import httpantry
import sys

def main():
    if len(sys.argv) == 1:
        print("help")
    else:
        arg = sys.argv[1]

        if arg == 'server':
            print("running server")
        else:
            print("help")