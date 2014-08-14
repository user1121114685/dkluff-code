#!/bin/sh
#get imgs from http://mm.dulei.si

logfile=/tmp/wgetimg.log
fetchlog=/tmp/fetchlog.log
dirprefix=`pwd`
getimgurl()
{
    imgarr=(`curl $1 | sed 's/href/\r/g' | grep -oi "http://mm.dulei.si/[^\"]*jpg"`)
    echo "$1 ${#imgarr[@]}" | tee -a $fetchlog
    for line in ${imgarr[@]}
    do
        echo "Getting $line"| tee -a $fetchlog
        wget -a $logfile -t 3 -nv $line &
    done
}

linenum=`cat $1 | grep ^# | wc -l | awk '{print $1}'`

for pg in `cat $1 | grep ^http`
do
    curdir=$dirprefix/`echo $pg | awk -F/ '{print $NF}'`
    mkdir -p $curdir
    echo "cd $curdir"
    cd $curdir

    getimgurl $pg
    pscount=`ps -ef | grep wget | grep -v grep | wc -l`
    while [ $pscount -lt 1 ]
    do
        pscount=`ps -ef | grep wget | grep -v grep | wc -l`
        echo "Getting: $pscount are working..."
    done

    echo "cd .. / leaving $curdir"
    cd ..

    linenum=$((linenum+1))
    sed -i "$linenum s/^/#/g" $1

    #echo "Stop in 5 sec..."
    #sleep 5

done
