#!/usr/bin/python
from string import Template
import socket
import os
def go():
  print("Starting Cassandra")
  f = open('/apache-cassandra/conf/cassandra.yaml.template', 'r')
  s = Template(f.read())
  f = open('/apache-cassandra/conf/cassandra.yaml', 'w')
  submap = os.environ.copy()

  if not 'INITIAL_TOKEN' in submap:
    submap['INITIAL_TOKEN'] = ''
  if 'PUBLIC_NAME' in submap:
    submap['BROADCAST_ADDRESS'] = socket.gethostbyname(submap['PUBLIC_NAME'])

  submap['LISTEN_ADDRESS'] = socket.gethostbyname(socket.gethostname())
  submap['SEEDS'] = submap['BROADCAST_ADDRESS']
  submap['RPC_ADDRESS'] = "0.0.0.0"
  f.write(s.substitute(submap))
  os.system("/apache-cassandra/bin/cassandra -f")

if __name__ == '__main__':
    go()
