#!/bin/bash
#file:runftp.sh 

#***********************************************
g_mmddlist=/tmp/mmddlist
g_yyyymmddlist=/tmp/yyyymmddlist
g_templist=/tmp/templist
#***********************************************

makedayslist(){
# $1 start date , $2 in days
# USAGE: makedayslist 20110501 7
date -s $1 >/dev/null
sys_curdate=`date +%Y%m%d`
echo "`date +%b.*%d`.*`date +%m%d`" > $g_mmddlist
date +%Y-%m-%d > $g_yyyymmddlist
for (( i=1; i<$2; i=i+1 )); do
        echo "`date +%b.*%d -d "-$i day"`.*`date +%m%d -d "-$i day"`" >>$g_mmddlist
	date +%Y-%m-%d -d "-$i day" >>$g_yyyymmddlist
done
date -s $sys_curdate >/dev/null
}
fetch_filelist_all(){
HOST='1.1.1.1'
USER='u'
PASSWD='1'
path=$1
ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
cd $path
ls
quit
END_SCRIPT
}

fetchftp(){
#USAGE: <ftp://u:p@host> </chn/ssl> </opt/logfile/> [jul]
ftpurl=$1
remote_dir=$2
workspace=$3

mkdir -p $workspace/ftptemp
tempdir=$workspace/ftptemp

echo "get the file list in $remote_dir ..."
fetch_filelist_all $remote_dir  | tee  $workspace/ftptemp/.filetoget_list_org
echo "cd $tempdir ..."
cd $tempdir
echo "get .filetoget_list_yes ..."
for DATE in `cat $g_mmddlist`; do
 cat $workspace/ftptemp/.filetoget_list_org | grep $DATE | awk '{print $NF}'
done | tee $workspace/ftptemp/.filetoget_list_yes

for line in `cat $workspace/ftptemp/.filetoget_list_yes` ; do
 echo  "`date` |fetch file |  $ftpurl/$remote_dir/$line" | tee -a  $g_templist
 #wget -c -t 2 -q --no-remove-listing -o $workspace/ftplog  "$ftpurl/$remote_dir/$line"
 wget -t 2 -q "$ftpurl/$remote_dir/$line"
done
}

cleanoldfiles(){
find /opt/logfile/ -type f -ctime +3 |  grep gz | xargs rm
}

##############main:
export LANG=en_US.UTF-8
if [[ -z $1 || -z $2 || -z $3 ]] ; then
 echo "USAGE: <curdate:20110601> <days:7>  <config file>"
 exit
else
 makedayslist $1 $2
 shift
 shift
 > $g_templist
 cleanoldfiles
 while [[ -n $1 ]] ; do
 
  cat $1 | while read LINE;
  do
   if [[  !( $LINE =~ ^# ) ]] ; then
    fetchftp $LINE
    echo "==`date` | finisded:| $LINE ==" | tee -a  $g_templist
   fi
  done

 shift
 done

fi
