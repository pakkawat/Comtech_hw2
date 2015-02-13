#!/usr/bin/python

import socket               # Import socket module
import os

def create_html_list(data):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>Directory listing for / </h1><hr><ul>"""
  for f in data:
    if f[0] != ".":
      temp += "<li><a href='http://" + socket.gethostname() + "cloudapp.net/" + f + "'>" + f + "</a></li>"

  temp += "</ul><hr>"
  return temp


def get_file(data):
  temp = []
  if len(data) == 2:
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    temp = files


  return create_html_list(temp)

def part_to_file(data):
  temp_start = 0
  temp_end = data.find("HTTP")

  if "GET" in data:
    temp_start = 4
    data = data[temp_start:temp_end]
    data = get_file(data)
  else: #DELETE
    temp_start = 7


  return data

def check_request(data):
  if "GET" in data:
    data = part_to_file(data)
  elif "DELETE" in data:
    data = part_to_file(data)
  elif "HEAD" in data:
    print "HEAD"

  return data
#------------------------------------------------------------
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 80                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr

   data = c.recv(1024)
   c.send(check_request(data))
   c.close()                # Close the connection
