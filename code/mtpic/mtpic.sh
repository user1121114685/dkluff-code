cd /home/dkluffy/mtpic
#t=`cat flist.txt|wc -l`
#h=$((RANDOM%$t))
#echo "h=$h"
if [ -e picsh.log ];then
    start=`tail -n 1 picsh.log | awk '{print $2}'`
else
    start=0
fi
echo "start: $start" >picsh.log
python picmt.py flist.txt $start |tee picsh.log

#mfile=`mktemp`
#cat pics.log | grep ^"#Movefile" | awk '{print $2}'> $mfile
#cat flist.ava.txt | grep -v -f $mfile > flist.tmp
#mv flist.tmp flist.ava.txt
#rm -f $mfile

