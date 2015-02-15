#!/usr/bin/python

import socket               # Import socket module
import os
import sys
import magic

def response_file(data,port):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>file </h1><hr>"""
  temp += data
  return temp

def response_html_list(data,port):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>Directory listing for / </h1><hr><ul>"""
  for f in data:
    if f[0] != ".":
      temp += "<li><a href='http://" + socket.gethostname() + ".cloudapp.net:" + port + "/" + f + "'>" + f + "</a></li>"

  temp += "</ul><hr>"
  return temp


def get_file(data,port):
  if len(data) == 2:
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    response_html_list(files,port)
  else:
    data = data[1:]
    return response_file(data,port)



def part_to_file(data,port):
  temp_start = 0
  temp_end = data.find("HTTP")

  if "GET" in data:
    temp_start = 4
    data = data[temp_start:temp_end]
    data = get_file(data,port)
  else: #DELETE
    temp_start = 7


  return data

def check_request(data,port):
  if "GET" in data:
    data = part_to_file(data,port)
  elif "DELETE" in data:
    data = part_to_file(data,port)
  elif "HEAD" in data:
    print "HEAD"

  return data
#------------------------------------------------------------
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])             # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr

   data = c.recv(1024)
   c.send(check_request(data,port))
   c.close()                # Close the connection
