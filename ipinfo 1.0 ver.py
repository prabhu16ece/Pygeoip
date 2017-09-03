# Author: Hades.y2k (github.com/Hadesy2k)
# Date: 14 July 2016
# Using ipinfo.io API (www.ipinfo.io/developers)


import requests
import socket
import sys


def main(ip):
    req = requests.get('http://ipinfo.io/' + ip).json()
    print "== INFORMATION =="
    for title in req:
        print title + ": " + req[title]


def usage():
    print "USAGE: python ipinfo.py (domain name / ip)"
    print "if you use domain name, do not put http://, just www.----.com\n"


def host2ip(host):
    return socket.gethostbyname(host)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit()
    else:
        if sys.argv[1].startswith('www'):
            ip = host2ip(sys.argv[1])
            main(ip)
        else:
            main(sys.argv[1])
