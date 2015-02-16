#!/usr/bin/python

import socket               # Import socket module
import os
import sys
import magic

def response_file(data,port):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>file </h1><hr>"""
  m = magic.open(magic.MAGIC_MIME_TYPE)
  m.load()
  temp += m.file(data[0:len(data)-1])
  return temp

def response_html_list(data,port):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>Directory listing for / </h1><hr><ul>"""
  for f in data:
    if f[0] != ".":
      temp += "<li><a href='http://" + socket.gethostname() + ".cloudapp.net:" + str(port) + "/" + f + "'>" + f + "</a></li>"

  temp += "</ul><hr>"
  return temp


def get_file(data):
  if len(data) == 2:
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    return response_html_list(files,port)
  else:
    data = data[1:]
    return response_file(data,port)



def part_to_file(data,start):
  end = data.find("HTTP")
  data = data[start:end]

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
   if not "favicon.ico" in data:
     if "GET" in data:
       path = part_to_file(data,4)
     elif "DELETE" in data:
       path = part_to_file(data,7)
     elif "HEAD" in data:
       print "HEAD"

     files = get_file(path)
     print files
     #c.send(check_request(data,port))
   c.close()                # Close the connection
