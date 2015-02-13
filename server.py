#!/usr/bin/python

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 80                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr

   data = c.recv(1024)
   print check_request(data)
   c.send("""HTTP/1.0 200 OK
Content-Type:text/html

<h1>Hello World</h1>""")
   c.close()                # Close the connection

def check_request(data):
  if "GET" in data:
    data = find_part_tp_file(data)
  elif "DELETE" in data:
    data = find_part_tp_file(data)
  elif "HEAD" in data:
    print "HEAD"

  return data

def find_part_to_file(data):
  temp_start = 0
  temp_end = data.find("HTTP")

  if "GET" in data:
    temp_start = 4
  else: #DELETE
    temp_start = 7

  data = [temp_start:temp_end]
  return data
