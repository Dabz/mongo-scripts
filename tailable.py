#!/bin/sh

##
## tailable.py
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Thu  7 Apr 17:15:04 2016 gaspar_d
## Last update Wed 27 Apr 11:39:13 2016 gaspar_d
##

import pymongo
import pprint
import time

def main():
    client = pymongo.MongoClient()
    collection = client.local.oplog.rs

    cursor = collection.find({}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT).max_await_time_ms(1000000)

    while (cursor.alive):
        try:
            doc = cursor.next()
            pprint.pprint (doc)
        except (StopIteration):
            print ('nothing, sleeping')

    time.sleep(1)

    print ('cursor is no longer alive, trying to reconnect')
    main()



main()
