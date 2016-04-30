#!/bin/sh

##
## parallelize_write.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Fri 22 Apr 13:34:01 2016 gaspar_d
## Last update Fri 29 Apr 10:30:31 2016 gaspar_d
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
import os


def infinite_insert(t, mongo):
    a = 1
    txt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1024*10))
    while True:
        try:
            mongo.test.test.insert_one({"thread": t, "number": a, "txt": txt})
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            pprint.pprint(time.ctime())
            pprint.pprint(repr(traceback.format_exception(exc_type, exc_value, exc_traceback, limit=2)))

            continue

def infinite_multi_insert(t, mongos):
    threads = []
    mongo = pymongo.MongoClient(mongos, maxPoolSize=100, waitQueueMultiple=1)
    for i in range(30):
        threads.append(threading.Thread(target=infinite_insert, args=("%s-%d" % (t, i), mongo)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


def main():
    for i in range(0, 100):
        mongos = "mongodb://root:root@127.0.0.1:20000,127.0.0.1:20001/admin"
        pid    = os.fork()
        if pid == 0:
            infinite_multi_insert("mongos-%d" % i, mongos)

main()
