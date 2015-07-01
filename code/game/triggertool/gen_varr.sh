grep -v ^$ | awk -v vname=$1 -v s=$2 ' BEGIN{a=s} {printf("set %s[%d] = '\''%s'\''\r\n",vname,a,$1);a=a+1}'
