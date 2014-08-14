#!/bin/sh
# This is a script for delete useless accesslist of cisco asa's configurations.
# Support asa ios version 8.3 and higher
# @Copyright by DKLuffy@gmail.com
# @Version:1.0
# @LastUpdate:2012-06-07

me=$0
func_usage(){
echo "\
    Usage:`echo $me` <file> <suffix> [max line(default 150)]
        *file: get file by [show access-list <name> ]
        *suffix: whatever, but remind that, there will be a dir named <suffix>
        *max line: you should provid this option, if the line(on config) exceed 150.
    "
}

#Init ...
if [[ ! (-e $1) || ! ($2) ]];then
    func_usage
    exit
fi
tmpwork=./$2
MAXLINES=150

if [[ ($3) && ($3 -gt 0) ]];then
    MAXLINES=$3
else
    echo "**No Max line or invalidate,use default($MAXLINES)."
fi

echo "*Splite the details by line of acl ..."
mkdir -p $tmpwork
for((i=1;i<$MAXLINES;i++));do
    cat $1 | grep "line $i " >$tmpwork/$i.$2.acl
done

resdir=$tmpwork/results
mkdir -p $resdir 

echo "*Fecth host results ..."
grep "hitcnt=0" $1 | grep -o "host [^ ]* " > $resdir/hosts_nohit.acl.$2.tmp
grep "hitcnt=[1-9][0-9]*)" $1 | grep -o "host [^ ]* " > $resdir/hosts_hashit.acl.$2
grep -v -f $resdir/hosts_hashit.acl.$2 $resdir/hosts_nohit.acl.$2.tmp|tee $resdir/hosts_nohit.acl.$2
echo

#identify the files
cd $tmpwork
mkdir -p unknown
mkdir -p hitcnt0
mkdir -p hashit

for f in `ls|grep ".acl$"`;do 
    h=`cat $f |sed '1d;s/(\|)\|hitcnt=//g' | awk '{a+=$(NF-1)}END{print a}'`; 
    if [[ ($h =~ [^0-9]) || ! ($h) ]];then 
        echo "unknown:"$f
        mv $f ./unknown/.
        continue
    fi
    if [ $h -eq 0 ];then 
        echo "hitcnt0:"$f
        mv $f ./hitcnt0/.
    else
        echo "hashit:"$f
        mv $f ./hashit/.
    fi
done

echo "*Dealing with unknown dir ..."
echo "   PS: The files in unknown dir has no more then 1 line"

cd unknown

for f in `grep -n -r "hitcnt=0" * | awk -F: '{print $1}' | sort -u`;do
    mv $f ../hitcnt0/.
done

for f in `grep -n -r "hitcnt=[1-9]*" * | awk -F: '{print $1}' | sort -u`;do
    mv $f ../hashit/.
done

echo "Leaving unknown dir ..."
cd ..
echo 

echo "*Getting the no hit acls <nohit.acl>..."
head -n 1 ./hitcnt0/* |grep ^acc | sed 's/(.*)//g;s/ 0x.*$//g;s/line [0-9]* //g;s/^/no /g'|tee nohit.acl.$2
echo "*Got `wc -l nohit.acl.$2` lines."
echo

echo "*Fetch obj groups info <obj_nohit.acl>..."
#
#cat nohit.acl.$2 | grep -o "object-group [^ ]* " | sort -u >obj_nohit.acl.$2.tmp
#cat ./hashit/* | grep -o "object-group [^ ]* " | sort -u >obj_hashit.acl.$2
cat nohit.acl.$2 | grep -o "object-group [^ ]*" | sort -u >obj_nohit.acl.$2.tmp
cat ./hashit/* | grep -o "object-group [^ ]*" | sort -u >obj_hashit.acl.$2
grep -v -f obj_hashit.acl.$2 obj_nohit.acl.$2.tmp \
    |sed 's/^/no /g;s/object-group/object-group network/g' | tee obj_nohit.acl.$2

echo "*Output patch for config..."
cat nohit.acl.$2 obj_nohit.acl.$2 > config.patch 

echo
echo "*Done ..."
echo "*Please find the patch file: `pwd`/config.patch."
echo "\
     **Warning: The results of object-groups should not been applied to the asa firewall 
        before being reviewed.
     "
echo

#NOTE FOR CLEAN NAT
#cat external.txt | grep hitcnt | awk '{gsub("[^0-9]","",$(NF-1));if($(NF-1)<100) print}' | grep -o "10\.[0-9\.]* " | sort -u > ht0.txt
#cat external.txt | grep hitcnt | awk '{gsub("[^0-9]","",$(NF-1));if($(NF-1)>=100) print}' | grep -o "10\.[0-9\.]* " | sort -u >ht1.txt
#cat ht0.txt | grep -v -f ht1.txt > noobj.txt && wc -l noobj.txt
