#!/usr/bin/python
from string import Template
import socket
import os
import subprocess
import etcd
import json
import time
import signal
import string

def go():
  f = open('/apache-cassandra/conf/cassandra.yaml.template', 'r')
  s = Template(f.read())
  f = open('/apache-cassandra/conf/cassandra.yaml', 'w')
  submap = os.environ.copy()
  print(submap)
  ip = socket.gethostbyname(socket.gethostname())
  print("ip:" + ip)
  client = etcd.Client(host=submap['SERVICE_HOST'])
  public_ip = ip # socket.gethostbyname(submap['COREOS_PUBLIC_IPV4'])
  submap['BROADCAST_ADDRESS'] = public_ip

  submap['LISTEN_ADDRESS'] = socket.gethostbyname(socket.gethostname())

  r = client.write("/services/cassandra", public_ip, append=True, ttl=30)
  time.sleep(1)

  sorted_results = list(sorted(client.read("/services/cassandra").children, key=lambda f:f.createdIndex))
  sorted_nodes = [str(n.value) for n in sorted_results]
  # up to the three oldest servers can be seeds. That seems reasonable.
  number_of_seeds = min(3, len(sorted_nodes))
  submap['SEEDS'] = string.join(sorted_nodes[:number_of_seeds], ", ")

  f.write(s.substitute(submap))
  proc = subprocess.Popen(["/apache-cassandra/bin/cassandra",  "-f"])

  signal.signal(signal.SIGINT, lambda s, f: proc.send_signal(signal.SIGINT))
  signal.signal(signal.SIGTERM, lambda s, f: proc.send_signal(signal.SIGTERM))

  while not proc.returncode:
    es_node = client.write(r.key, public_ip, append=False, ttl=30).value
    time.sleep(20)
    proc.poll()

if __name__ == '__main__':
    go()
