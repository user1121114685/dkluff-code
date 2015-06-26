#!/bin/sh


rblock(){
  sed 's///g' | sed -e '/./{H;$!d;}' -e "x;/\[$1\]/b" -e d
}

delblock(){
  sed 's///g' | sed -e '/./{H;$!d;}' -e "x;/\[$1\]/d;b"
}

modopt(){
    f=$1
    shift
    while [ $2 ];do
        sed -i -e "s/^$1.*$/$2/g" -e 's/|p/\\/g' $f
        shift
        shift
    done
}

prctxt(){
    srcf=$1
    shift
    arg=""
    orgname=""
    newname=""
    optname=""
    optvalue=""
    
   if [[ ! -z `echo $@ | grep "\-a \|\-on \|\-optn \|\-optv \|-nn "` ]]; then
       while [ $1 ];do
           [[ -z `echo $@ | grep "\-a \|\-on \|\-optv \|-nn "` ]] && break
           [ "$1" == "-a" ] && shift && arg=$1 && shift
           [ "$1" == "-on" ] && shift && orgname=$1 && shift
           [ "$1" == "-nn" ] && shift && newname=$1 && shift
           [ "$1" == "-optn" ] && shift && optname=$@ && break
        done
    else
        orgname=$1
        shift
        newname=$1
        shift
        optname=$@
    fi

    if [ "$orgname" == "-" ] ;then
       cat $srcf | delblock $newname
       return 
    fi
    
    tmpf=`tempfile`
    
    cat $srcf | rblock $orgname| sed -e "s/\[$orgname\]/\[$newname\]/g" > $tmpf

    if [[ ! -z $optname ]];then 
        modopt $tmpf $optname
    fi
    cat $tmpf
    
    rm -f $tmpf
}

#prctxt $@ 
#$1 org file
#$2 cmdfile
tmpfile=`tempfile`
tmpfile2=`tempfile`
tmpfile3=`tempfile`

cp -f $1 $tmpfile2

cat $2 |grep -v ^# | grep -v ^\- | while read l;do
    prctxt $1 $l >>$tmpfile 
done
cat $2 |grep -v ^# | grep  ^\- | while read l;do
    prctxt $tmpfile2 $l >$tmpfile3
    cp -f $tmpfile3 $tmpfile2
done

cat $tmpfile  
cat $tmpfile2


rm -f $tmpfile
rm -f $tmpfile2
rm -f $tmpfile3

    





