#!/bin/sh
cmd=$1

cp -f org.db all.db
../bin/4itemdpatcher.sh $cmd
../bin/totxt.sh

cat $cmd | grep ^kis | sed 's/^kis //g' | grep cp >ItemData.slk.cook
cat $cmd | grep ^kis | sed 's/^kis //g' | grep -v cp >>ItemData.slk.cook
../bin/prslk.py ItemData.slk ItemData.slk.cook >./data/ItemData.slk

cp -f ./data/* /root/otg_game/uwin/.
