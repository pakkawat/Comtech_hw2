#!/usr/bin/python

import socket               # Import socket module
import os
import sys
import magic

def http_bad_request():
  return 'HTTP/1.0 400 Bad Request\nContent-Type:text/html\n\n<h1>HTTP 400 Bad Request</h1>'

def response_header_202():
  return 'HTTP/1.0 202 Accept\nContent-Type:text/html\n\n<h1>HTTP 202 Accept</h1>'

def response_header_204():
  return 'HTTP/1.0 204 No Content\nContent-Type:text/html\n\n<h1>HTTP 204 No Content</h1>'

def response_header_404():
  return 'HTTP/1.0 404 Not Found\nContent-Type:text/html\n\n'

def response_header_200():
  return 'HTTP/1.0 200 OK\nContent-Type:text/html\n\n'

def response_html_404():
  return 'HTTP/1.0 404 Not Found\nContent-Type:text/html\n\n'

def response_header_file(file_name):
  temp = 'HTTP/1.0 200 OK\n'
  m = magic.open(magic.MAGIC_MIME_TYPE)
  m.load()
  temp += 'Content-Type: ' + m.file(file_name[0:len(file_name)-1]) + '\n'
  temp += 'Host: ' + socket.gethostname() + '.cloudapp.net\n'
  f = open(file_name[0:len(file_name)-1])
  outputdata = f.read()
  temp += 'Content-Length: ' + str(len(outputdata)) + '\n\n'
  return temp


def response_html_list(files):
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

def delete_request(c,data):
  path = part_to_file(data,7)
  files = get_file(path)
  if type(files) == type(str()):
    if os.path.isfile(files[0:len(files)-1]):
      os.remove(files[0:len(files)-1])
      c.send(response_header_204())
    else:
      c.send(response_header_202())

def head_request(c,data):
  path = part_to_file(data,5)
  files = get_file(path)
  if type(files) == type(list()):
    c.send(response_header_200())
  elif type(files) == type(str()):
    if os.path.isfile(files[0:len(files)-1]):
      c.send(response_header_200())
    else:
      c.send(response_header_404())


def get_request(c,data):
  path = part_to_file(data,4)
  files = get_file(path)
  if type(files) == type(list()):
    outputdata = response_html_list(files)
    c.send(outputdata)
  elif type(files) == type(str()):
    if os.path.isfile(files[0:len(files)-1]):
      header = response_header_file(files)
      f = open(files[0:len(files)-1])
      outputdata = f.read()
      c.send(header)
      for i in range(0, len(outputdata)):
        c.send(outputdata[i])
    else:
      header = response_html_404()
      c.send(header)

#------------------------------------------------------------
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])             # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   #print 'Got connection from', addr

   data = c.recv(1024)
   if not "favicon.ico" in data:
     if "GET" in data:
       get_request(c,data)
     elif "DELETE" in data:
       delete_request(c,data)
     elif "HEAD" in data:
       head_request(c,data)
     else:
       c.send(http_bad_request())



   c.close()                # Close the connection
