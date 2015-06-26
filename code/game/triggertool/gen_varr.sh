cat $1 | grep -v ^$ | awk -v vname=$2 -v s=$3 ' BEGIN{a=s} {printf("set %s[%d] = '\''%s'\''\r\n",vname,a,$1);a=a+1}'
