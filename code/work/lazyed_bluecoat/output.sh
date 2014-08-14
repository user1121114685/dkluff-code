#!/bin/bash
while [[ -n $1 ]];do
    logroot=`cat $1 | grep -v ^# | awk '{print $NF}' | sed '1!d;s/cifs\|main\|ssl//g'`
    if [ -e $logroot ];then
        echo "Info: LogRoot= $logroot,working..."
        /usr/bin/py27 lazed.py $logroot
    else
        echo "Error: LogRoot not exists!"
    fi
    shift
done
