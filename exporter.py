from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import os
import socket
import time
import pathlib
from pathlib import Path
from datetime import date, timedelta
# Author: Ownercz 
# Contact: radim@lipovcan.cz
# Tested with RPI 2B+ running Raspbian Buster
# Crontab entry:
# @reboot /usr/bin/screen -dmS exporter /usr/bin/python3 "/home/pi/exporter.py"
def gettemp():
        html = []
        errorfile = pathlib.Path("/tmp/maillog.error")
        html.append("# HELP onewire A summary of the GC invocation durations.")
        html.append("# TYPE onewire gauge")
        past_time = time.time() - 90
        if(os.path.isfile(errorfile)):
          html.append('postfix_error{hostname="' + socket.gethostname() + '"} ' + '1')
          timestamp = os.path.getctime(errorfile)
          if errorfile.is_file() and past_time > timestamp:
            errorfile.unlink() # Delete files
            print("this is older")
            try:
              #path.rmdir() # Delete empty folders
              pass
            except (FileNotFoundError, WindowsError):
              pass
          else: 
            print("too early")
            print(timestamp)
            print(past_time)
        else: 
          html.append('postfix_error{hostname="' + socket.gethostname() + '"} ' + '0')

            
#        print(html)
        return html

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  def handle(self):
      try:
          BaseHTTPRequestHandler.handle(self)
      except socket.error as err:
          pass
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/plain')
        self.end_headers()

        # Send message back to client
        message = '\n'.join(map(str, gettemp()))
        #message = gettemp()
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', 9160)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
