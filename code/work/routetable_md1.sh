#!/bin/bash
#add names to route table
[ -e $1 ] || exit
[ -e $2 ] || exit
[ -e $3 ] || exit

subnetlist=$1
#
#192.168. CustomerVPN
#

devlist=$2
#
#192.62.11.1   Route1
#

routetable=$3
#
#ip route 0.0.0.0 0.0.0.0 192.1.1.1
#
tmpfile=$(tempfile) || exit

declare -A tmparr
###cat $devlist | while read d;do  #subshell can't modify global var
lbread(){
while read d; do
  name=$(echo $d | awk '{print $2}')
  ip=$(echo $d | awk '{print $1}')
  tmparr["$ip"]=$name
done < $1
}

#replace dev name
lbread $devlist

while read rt;do
devi=$(echo $rt | awk '{print $5}')
if [ -z ${tmparr["$devi"]} ];then
  tmparr["$devi"]="Unknow"
fi
echo $rt | awk -v devi=$devi -v devn=${tmparr["$devi"]} '{sub(devi,$NF" ["devn"]",$NF);print }'
done < $routetable >$tmpfile

tmparr=()
lbread $subnetlist
while read rt;do
  subnet=$(echo $rt | awk '{split($3,sn,".");print sn[1]"."sn[2]"."}')
  if [ -z ${tmparr["$subnet"]} ];then
    tmparr["$subnet"]="Unknow"
  fi
  echo $rt | awk -v subnet=$subnet -v name=${tmparr["$subnet"]} '{ 
    split($3,rt,".");split(subnet,sn,".");
    if(rt[0] == sn[0] && rt[1]==sn[1]){
      $4=$4"["name"]"
      print
    }
  }'
done <$tmpfile

rm -f $tmpfile
