#!/usr/bin/python

import socket               # Import socket module
import os
import sys
import magic

def response_header_file(file_name):
  temp = 'HTTP/1.0 200 OK\n'
  m = magic.open(magic.MAGIC_MIME_TYPE)
  m.load()
  temp += 'Content-Type: ' + m.file(data[0:len(data)-1]) + '\n'
  temp += 'Host: ' + socket.gethostname() + '.cloudapp.net\n'
  f = open(file_name[0:len(file_name)-1])
  outputdata = f.read()
  temp += 'Content-Length: ' + len(outputdata) + '\n'
  return temp

def response_header_html_list(files):
  temp = """HTTP/1.0 200 OK
Content-Type:text/html

<h1>Directory listing for / </h1><hr><ul>"""
  for f in files:
    if f[0] != ".":
      temp += "<li><a href='http://" + socket.gethostname() + ".cloudapp.net:" + str(port) + "/" + f + "'>" + f + "</a></li>"

  temp += "</ul><hr>"
  return temp


def get_file(path):
  if len(path) == 2:
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    return files
  else:
    path = path[1:]
    return path



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

     header = ''
     files = get_file(path)
     if type(files) == type(list()):
       header = response_header_html_list(files)
       c.send(header)
     elif type(files) == type(str()):
       header = response_header_file(files)
       f = open(files[0:len(files)-1])
       outputdata = f.read()
       c.send(header)
       c.send(outputdata)
     
   c.close()                # Close the connection
