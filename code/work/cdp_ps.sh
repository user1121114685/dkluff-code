#!/bin/sh
tmpfile="tmpfile"
prefix="pretmp_"
cat $1 | grep "Device ID\|Platform\|Interface\|IP address" > $tmpfile
split $tmpfile $prefix -l 5
sed -i 's/,/\n/g' $prefix*
for f in `ls | grep $prefix `;do cat $f | awk -F: '{gsub(/^ /,"",$2);a[$1]=$2} END {for( i in a) printf "%s,",a[i];printf "%s\n","" }'; done | sed 's/.microstrategy.com//g' >>$1.output.csv
rm -f $tmpfile
rm -f $prefix*
