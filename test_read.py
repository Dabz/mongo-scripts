#!/bin/sh

##
## test_read.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Tue  1 Mar 10:11:35 2016 gaspar_d
## Last update Wed 27 Apr 14:31:29 2016 gaspar_d
##

import pymongo
import time

def main():
  mongo = pymongo.MongoClient('mongodb://localhost:27017/?replicaSet=tisco&readPreference=primary')
  while 1:
    try:
      c = mongo.test.test.find_one()
      print('read: success')
    except Exception as e:
      print('read: failed')
      print(e)
    time.sleep(0.5)


main()
