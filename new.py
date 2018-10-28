from model import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import pdb
import uuid

hostName = "0.0.0.0"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.get_qs()
        if 'reading' in self.path:
            if 'new' in self.path:
                self.new_reading()
        else:
            if 'new' in self.path:
                self.write()
            if 'find' in self.path:
                self.lookup()
            
    def new_reading(self):
        self.report = SoundReport()
        self.report.id = self.id()
        self.report.reading(self.parse_reading())

    def parse_reading(self):
        self.get_qs()
        num = self.queryString['num']
        carclass = self.queryString['carclass']
        reading = self.queryString['reading']
        return [num, carclass, reading]

    def id(self):
        self.get_qs()
        return self.queryString['id']

    def get_qs(self):
        self.queryString = parse_qs(urlparse(self.path).query)
        for key, value in self.queryString.items():
            if value[0].isdigit():
                self.queryString[key] = int(value[0])
            else:
                self.queryString[key] = value[0]

    def lookup(self):
        self.report = SoundReport()
        self.report.id = self.id()
        self.report.read()
        self.debug()
        self.wfile.write(bytes(str(self.report.__dict__), "utf-8"))

    def debug(self):
        self.wfile.write(bytes("<p>Query string: %s</p>" % self.queryString, "utf-8"))
        self.wfile.write(bytes("<p>URL Parse: %s</p>" % urlparse(self.path).query, "utf-8"))

    def write(self):
        self.debug()
        self.report = SoundReport()
        for key, value in self.queryString.items():
            self.report.__dict__[key] = value
            self.report.id = 1
        self.report.save()

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
