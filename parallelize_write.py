#!/bin/sh

##
## parallelize_write.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Fri 22 Apr 13:34:01 2016 gaspar_d
## Last update Mon  9 May 07:48:53 2016 gaspar_d
##

import pymongo
import sys
import thread
import threading
import time
import random
import string
import pprint
import traceback
import logging
import os
import sys


def infinite_insert(t, mongo):
    a = 1
    txt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    collection = mongo.test.test
    while True:
        try:
            collection.insert_one({"thread": t, "number": a, "txt": txt})
        except Exception as e:
            logging.exception("Ohh noes!!!")
            time.sleep(1)
            continue

def infinite_multi_insert(t, mongos):
    threads = []
    mongo = pymongo.MongoClient(mongos, maxPoolSize=30, waitQueueMultiple=2, connect=False)
    for i in range(30):
        threads.append(threading.Thread(target=infinite_insert, args=("%s-%d" % (t, i), mongo)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def main(num_proc, fork=False):
    for i in range(0, num_proc):
        mongos = "mongodb://app:app@172.17.0.1:27017/admin"
        if fork:
          pid = os.fork()
          if pid == 0:
              infinite_multi_insert("mongos-%d" % i, mongos)
        else:
          infinite_multi_insert("mongos-%d" % i, mongos)

main(int(sys.argv[1]))
