#!/usr/bin/python
from string import Template
import os
def go():
  print("Starting Cassandra")
  f = open('/apache-cassandra/conf/cassandra.yaml.template', 'r')
  s = Template(f.read())
  f = open('/apache-cassandra/conf/cassandra.yaml', 'w')
  substitution_map = os.environ.copy()
  # TODO: munge map
  if substitution_map['SEEDS'] == '':
    substitution_map['SEEDS'] = '127.0.0.1'
  if not 'INITIAL_TOKEN' in substitution_map:
    substitution_map['INITIAL_TOKEN'] = ''

  f.write(s.substitute(substitution_map))
  os.system("/apache-cassandra/bin/cassandra -f")

if __name__ == '__main__':
    go()
