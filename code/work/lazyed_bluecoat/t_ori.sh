#!/bin/bash
orionlogroot="/tmp/orion"
curdir=`pwd`
cd $orionlogroot
cat fw-outside.csv | grep -v "^#\|Node" |\
    awk -F, '{gsub("\\..*$","",$1);print $1,$11}' |\
    sed 's/[Tt][Bb]"/1099511627776/g;s/[Gg][Bb]"/1073741824/g;s/[Mm][Bb]"/1048576/g;s/[Kk][Bb]"/1024/g;s/"//g' |\
    awk '{print $1,$2*$3}' \
    >fw-bytes.log
    
>fw-b.log
cat fw-bytes.log | grep -i chn | grep -vi bj | awk '{k+=$2}END{print "CTC",k}' >>fw-b.log
cat fw-bytes.log  | grep -i arg-asa | awk '{k+=$2}END{print "ARG",k}' >>fw-b.log
cat fw-bytes.log  | grep -i ash-.*asa | awk '{k+=$2}END{print "ASH",k}' >>fw-b.log
cat fw-bytes.log  | grep -i brz | awk '{k+=$2}END{print "BRZ",k}' >>fw-b.log
cat fw-bytes.log  | grep -i pol | awk '{k+=$2}END{print "POL",k}' >>fw-b.log
cat fw-bytes.log  | grep -i syd | awk '{k+=$2}END{print "SYD",k}' >>fw-b.log
cat fw-bytes.log  | grep -i sin | awk '{k+=$2}END{print "SIN",k}' >>fw-b.log
echo "SAF 0" >>fw-b.log


cd $curdir
