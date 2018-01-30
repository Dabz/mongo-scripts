#!/bin/sh

##
## test_read.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Tue  1 Mar 10:11:35 2016 gaspar_d
## Last update Tue  1 Mar 10:46:07 2016 gaspar_d
##

import pymongo
import time

def main():
  while 1:
    try:
      c = mongo.test.test.insert_one({"a": 1})
      print('write: success')
    except Exception as e:
      print('write: failed')
      print(e)
    time.sleep(0.5)

    def retry():
  mongo = pymongo.MongoClient('mongodb://localhost:27017/?replicaSet=test&readPreference=primaryPreferred')
  while 1:
    try_count = 2
    while try_count > 0:
      try:
        c = mongo.test.test.insert_one({"a": 1})
        break;
      except Exception as e:
        print('retrying (left %d), exception: %s' % (try_count, e))
        try_count -= 1
    if try_count > 0:
      print('write: success')
    else:
      print('write: failed')

    time.sleep(0.5)

retry()
