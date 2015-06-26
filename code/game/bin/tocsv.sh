#!/bin/sh


rblock(){
  sed 's///g' | sed -e '/./{H;$!d;}' -e "x;/\[$1\]/b" -e d
}

delblock(){
  sed 's///g' | sed -e '/./{H;$!d;}' -e "x;/\[$1\]/d;b"
}

txtTocsv(){
    cat $1 |grep -v "^//\|^$" | rblock $3 | sed '/^$/d' | sed 's/ //g' |awk -v f="$2" 'BEGIN{printf("%s ",f) } { printf("%s ",$1)} END{printf("\n")}'
}

namelist=$1/csvlist.txt
filelist=$1/csvfilelist.txt


cat $namelist | grep -o "[a-zA-Z0-9]*" | while read n;do
    for k in `cat $filelist | grep -v ^# | grep -v ^$`;do
        txtTocsv $1/data/$k $k $n 
    done

done

