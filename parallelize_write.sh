#!/bin/sh

##
## parallelize_write.sh
##
## Made by gaspar_d
## Login   <d.gasparina@gmail.com>
##
## Started on  Thu  5 May 11:37:46 2016 gaspar_d
## Last update Thu  5 May 23:18:53 2016 gaspar_d
##


NUM_PROCESS=$1
TYPE=$2

pkill -9 dstat
rm -rf logs/* dstat/*
mkdir logs 2> /dev/null
mkdir dstat 2> /dev/null

export DSTAT_MONGODB_PWD=app
export DSTAT_MONGODB_USER=app
nohup dstat -t -a --tcp --mongodb-opcount --mongodb-conn --out dstat/perf.csv 2>&1 > /dev/null &

for i in `seq $NUM_PROCESS`; do
  if [[ "$TYPE" == "docker" ]]; then
    docker run -d -v $PWD:/home/ec2-user/ -t pymongo -c "cd /home/ec2-user/; python parallelize_write.py 1 2>&1 > logs/log_$i.log"
  else
    nohup python parallelize_write.py 1 2>&1 > logs/log_$i.log &
  fi
  sleep 10
done

sleep 5
