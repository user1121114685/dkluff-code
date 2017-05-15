#!/bin/sh
filename="/Users/dkluffy/Documents/db-stock.txt"
showsold=""
dosave=""

if [ $1 ];then
  filename=$1
  showsold=$2
  dosave=$3
fi
codelist=$filename

api="http://hq.sinajs.cn/list="

getcurprice(){
  while read line
  do
    name=`echo $line| awk '{print $1}'`
    code=`grep "^#codes.*${name:1}" $codelist | awk '{printf("%s",$3)}'`
    code=${code[@]//[^A-Za-z0-9]/}
    price=0
    if [ $code ];then
      price=$(curl -s "$api$code" | awk -F, '{print $4}')
    fi
    echo $line | awk -v p=$price '{print $0,p,(p-$4)*$2,100*(p-$4)/$4"%";}'
    #echo $line | awk -v p=$price '{printf "s% .2f% .2f% .2f%\n",$0,p,(p-$4)*$2,100*(p-$4)/$4;}'
  done
}


fmtdata(){
#awk: split(k,idx,SUBSEP);
cat $filename | grep -v "^#" | awk '
  {a[$2]+=$5;b[$2]+=$4*$5;}
  END {
  for( k in a){
    name=k;
    price=0;
    if(a[k]>0) name="*"k;
    if(a[k]>=100) price=b[k]/a[k];
    print name,a[k],-1*b[k],price;
  }
 }' | sort -k 3 -nr | while read line;do
   amount=$(echo $line | awk '{print $2}')
   if [ $amount -lt 100 ];then
     echo $line
   else
     echo $line | getcurprice
   fi

   done
}

prtsum(){

  if [ $showsold ];then
    fmtdata
  else
    fmtdata | awk '{if($2>=100) print $0;}'
    echo "...sold stocks are trunked..."
  fi
  echo
  echo
  echo "***Sum***"

  fmtdata | awk '
  BEGIN { totalcash=0;totalgain=0}
  {
    if(match($1,"现金")>0) totalcash=$3;
    else
      if($2>=100) totalgain+=$6;
      else totalgain+=$3
  }
  END { printf "#TotalCash=%.2f; TotalGain=%.2f; TotalValue=%.2f\n",totalcash,totalgain,totalcash+totalgain;
        printf "#*****(%.2f)%%",totalgain*100/totalcash;
      }
  '
}




result=$(prtsum)
echo "$result"

if [ $dosave ];then
  r=$(echo "$result" | sed '/^#Total/!d;s/#//g')
  eval $r
  sh000001=$(curl -s "$api""sh000001" | awk -F, '{print $4}')
  echo "#p1|$TotalValue|$sh000001|$TotalGain$(date "+|%Y/%m/%d")" | tee -a $filename
fi


#-----#
echo "-#Usage: ./clistocktool.sh filename showold dosave "



