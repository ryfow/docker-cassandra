#!/usr/bin/python
from string import Template
import socket
import os
import etcd
import json
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

  if 'INITIAL_NODE' in submap and submap['INITIAL_NODE'] == "true":
    submap['SEEDS'] = submap['BROADCAST_ADDRESS']
  else:
    client = etcd.Client(host=submap['PUBLIC_NAME'])
    cas1_json = client.get("/services/cassandra/cassandra1").value
    cas1_dict = json.loads(cas1_json)
    cas1_host = cas1_dict['host']
    submap['SEEDS'] = socket.gethostbyname(cas1_host)

  f.write(s.substitute(submap))
  os.system("/apache-cassandra/bin/cassandra -f")

if __name__ == '__main__':
    go()
