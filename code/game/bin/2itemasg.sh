#!/bin/sh

newitem(){
echo "
ratf I0A1 A0a1 攻击之爪-I0 增加攻击
clfm I0A2 A0b1 龙血风衣-I0 加一定跑速度，并增加防御
rugt I0A3 A0a2,A0a1 爆裂血爪-I0 加攻击，加暴击
ratf I0B1 A0a5,A0a6 龙骨弓-I0 远程可以多重攻击，并加攻击速度 ReplaceableTextures/CommandButtons/BTNSkeletalLongevity.blp
ratf I0B2 A0a5,A0a3 龙鳞枪-I0 近战可以分裂攻击，并加攻击速度 ReplaceableTextures/PassiveButtons/PASBTNCleavingAttack.blp

"

}

prtfromItemtemplate(){

newitem | grep -v ^#| grep -v ^$ | while read l
do
    i=1
    while [ $i -lt 10 ];do
        echo $l | sed "s/I0/I$i/g;s/A0/A$i/g" 
        i=$((i+1))
    done
done
}

echotamplate(){
echo "
kis #orgname 1 \"#newname\" cp
kis #newname 8 \"#abi1\" 
1kit itemstrings.txt [#newname] Name=#chname Tip=购买|cffffcc00#chname|r Ubertip=\"#iutip,DATA-|cffffcc00<#abi2,DataA1>|r\" 
"
}

assignAbi(){
    while read l
    do
        a=`echo $l | awk '{ print $1}'`
        b=`echo $l | awk '{ print $2}'`
        c=`echo $l | awk '{ print $3}'`
        d=`echo $l | awk '{ print $4}'`
        e=`echo $l | awk '{ print $5}'`
        f=`echo $l | awk '{ print $6}'`
        abi=`echo $c | awk -F, '{print $1}'`

        if [ $f ];then
            echotamplate| grep -v ^$ | sed "s/#orgname/$a/g;s/#newname/$b/g;s/#abi1/$c/g;s/#chname/$d/g;s/#abi2/$abi/g;s/#iutip/$e/g;"
            echo "2kit ItemFunc.txt [#newname] Art=#newart" | sed "s/#newname/$b/g;s:#newart:$f:g;" | sed 's:\/:\\:g' 
        else
            echotamplate| grep -v ^$ | sed "s/#orgname/$a/g;s/#newname/$b/g;s/#abi1/$c/g;s/#chname/$d/g;s/#abi2/$abi/g;s/#iutip/$e/g;s/#newart/$f/g"
            echo "#- $a $b"
        fi
        echo
    done
}

prtfromItemtemplate | assignAbi 
