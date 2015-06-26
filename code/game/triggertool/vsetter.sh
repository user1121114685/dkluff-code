#!/bin/sh

vlist=$1
a=0

ty="udg_temparrinteger"

cat $1 | while read line
do
    t=`echo $line | awk '{print $1}'`
    v=`echo $line | awk '{print $2}'`

    if [ "$v" = "array" ]
    then
        continue
    fi

    if [ "$t" = "real" ] 
    then
        ty="udg_temparrreal"
    elif [ "$t" = "integer" ]
    then
        ty="udg_temparrinteger"
    else
        continue
    fi

    echo "set $ty[$a] = $v"

    a=$((a+1))
done

echo
echo "set udg_temparrinteger[j] = e"
echo "set udg_temparrreal[j] = e"
echo

cat $1 | while read line
do
    t=`echo $line | awk '{print $1}'`
    v=`echo $line | awk '{print $2}'`

    if [ "$v" = "array" ]
    then
        continue
    fi

    if [ "$t" = "real" ] 
    then
        ty="udg_temparrreal"
    elif [ "$t" = "integer" ]
    then
        ty="udg_temparrinteger"
    else
        continue
    fi

    echo "set $v = $ty[$a]"

    a=$((a+1))
done

echo
echo

oty="I2S"
cat $1 | while read line
do
    t=`echo $line | awk '{print $1}'`
    v=`echo $line | awk '{print $2}'`

    if [ "$v" = "array" ]
    then
        oty="I2S"
        continue
    fi

    if [ "$t" = "real" ] 
    then
        ty="udg_temparrreal"
        oty="R2S"
    elif [ "$t" = "integer" ]
    then
        ty="udg_temparrinteger"
    else
        continue
    fi

    echo "set udg_qstr[$a]= \"REG $a @$v = \" + $oty( $v) "
    a=$((a+1))
done

echo "call debugmsg(\"REG SET DONE!\")"

