#!/bin/sh

##
## monto_utils.sh
##
## Made by Gasparina Damien
## Login   <gaspar_d@epita.fr>
##
## Started on  Sun 29 Nov 20:41:26 2015 Gasparina Damien
## Last update Sun 29 Nov 21:33:55 2015 Gasparina Damien
##

MONGO_MOUNT_POINT=/data/
MONGO_BLOCKDEV=/dev/sdb
MONGO_DB=test
MONGO_COLLECTION=sym_data
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_PADDING_SIZE=256

function clean_fs_cache() {
  echo 3 >> /proc/sys/vm/drop_caches
}

function create_fs() {
  if [ `mount | grep $MONGO_MOUNT_POINT | wc -l` -gt '0' ]; then
    mkfs.xfs $MONGO_BLOCKDEV
    rm -rf $MONGO_MOUNT_POINT
    mkdir $MONGO_MOUNT_POINT
    mount ${MONGO_BLOCKDEV} $MONGO_MOUNT_POINT
  fi
}

function install_mongod() {
  if [ ! -f /etc/yum.repos.d/mongodb.repo ]; then
    echo > /etc/yum.repos.d/mongodb.repo << EOF
    [mongodb-org-3.0]
    name=MongoDB Repository
    baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.0/x86_64/
    gpgcheck=0
    enabled=1
EOF
    yum update
    yum install mongodb-org
  fi
}

function insert_sample_data() {
  database=$1
  collection=$2
  number_of_doc=$3
  number_of_thread=$4

  for i in `seq 1 $4`; do
    python -c '
      import pymongo, sys;

      var mongo_connection = sys.argv[1]
      var mongo_db         = sys.argv[2]
      var mongo_collection = sys.argv[3]
      var number_of_doc    = sys.argv[4]
      var number_of_thr    = sys.argv[5]
      var thread_num       = sys.argv[6]
      var padding          = sys.argv[7]
      var doc_per_thread   = number_of_doc / number_of_thr
      var client           = MongoClient(mongo_connection)
      var collection       = client[mongo_db][mongo_collection]

      for doc_num in range(doc_per_thread * thread_num, (doc_per_thread + 1) * thread_num):
        collection.insert({"_id": doc_num, "padding": padding})
    '  "$MONGO_HOST:$MONGO_PORT" $MONGO_DB $MONGO_COLLECTION $number_of_doc $number_of_thr $i `openssl rand -base64 $MONGO_PADDING_SIZE`&
  done
}

function start_mongod() {
  if [ `pidof mongod` == "" ]; then
    mongod --fork --logpath /var/log/mongod.log --dbpath /data
  fi
}
