#!/bin/sh

##
## mass_delete_opsmgr.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Fri 22 Apr 16:35:14 2016 gaspar_d
## Last update Sat 30 Apr 19:20:19 2016 gaspar_d
##

import urllib2
import json
import requests
import sys

u    = sys.argv[1]
p    = sys.argv[2]
url  = 'https://cloud.mongodb.com/api/public/v1.0/groups/56780852e4b01bbe940b8458/hosts'
auth = requests.auth.HTTPDigestAuth(u, p)

page_content = requests.get(url, auth=auth)
content  = page_content.json()
toDelete = []

for host in content['results']:
    toDelete.append(host)

for host in toDelete:
    url = 'https://cloud.mongodb.com/api/public/v1.0/groups/56780852e4b01bbe940b8458/hosts/%s' % host['id']
    page_content = requests.delete(url, auth=auth)
    print(page_content.json())
