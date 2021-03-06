#!/usr/bin/env python

import os
import sys
import getopt
import json
from pprint import pprint

def creatVirtualHost(id, protocol, proxy, subdomain, instance, url, portnumber, instancepath):
    print("Create VirtualHost for " + id)

    instanceTemplateFileName = instancepath + '/virtualhost_' + protocol.lower() + '.template';

    templateFileName = 'config/virtualhost_' + protocol.lower() + '.template';

    if os.path.exists(instanceTemplateFileName):
        templateFileName = instanceTemplateFileName

    virtualhost = open(templateFileName, 'r').read()
    virtualhost = virtualhost.replace("§§subdomain", subdomain.replace('§§INSTANCE', str(instance)).lower())
    virtualhost = virtualhost.replace("§§url", str(url))
    virtualhost = virtualhost.replace("§§ip", "127.0.0.1")
    virtualhost = virtualhost.replace("§§port", str(portnumber))
    print(virtualhost)
    return virtualhost


print ("SETUP UP PORT")

argv = sys.argv[1:]
opts, args = getopt.getopt(argv,"a:i:",["applicationpath=","instancepath="])
for opt, arg in opts:
    if opt == '-h':
        print('test.py -a <applicationpath> -i <instancepath>')
        sys.exit()
    elif opt in ("-a", "--applicationpath"):
        applicationpath = arg.strip()
    elif opt in ("-i", "--instancepath"):
        instancepath = arg.strip()

with open(instancepath + '/portinfo.json') as data_file:
    ports = json.load(data_file)
with open(instancepath + '/portmap.json') as data_file:
    portsmapping = json.load(data_file)

pprint(portsmapping)

baseurl = portsmapping['baseurl']
instance = portsmapping['instance']

virtualhost = ""

for port in ports['mappings']:
    virtualhost += "\n"+creatVirtualHost(port['id'], port['protocol'], port['proxy'], port['url'], instance, baseurl, portsmapping[port['id']], instancepath)

target = open("/etc/apache2/sites-available/005-" + instance, 'w')
target.write(virtualhost)
target.close()

os.symlink("/etc/apache2/sites-available/005-" + instance, "/etc/apache2/sites-enabled/005-" + instance)


