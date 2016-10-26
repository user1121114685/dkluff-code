#!/bin/sh

url="https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
dst="/etc/hosts"
dstdate=$(sed '/^# Last updated:/!d;s/[^0-9]//g' $dst )
urlfile=$1
if [ ! $1 ];then
 urlfile=$(curl -k $url)
fi
urldate=$( echo "$urlfile" | sed '/^# Last updated:/!d;s/[^0-9]//g' )


echo "$dstdate""::::""$urldate"

read -p "1/yes,0/no...::" a
if [ $a -eq 0 ];then
  exit 0
fi

filedump(){
  sed '1,10!d' $dst
  [ -f $1 ] && cat $1
  [ ! -f $1 ] && echo $urlfile

}

echo "dumping..."

filedump $1 > $dst
