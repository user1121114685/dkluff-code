#!/bin/sh
cmd=$1

#cp -f org.db all.db
#../bin/3abidbpatcher.sh $cmd
#../bin/totxt.sh

cat $cmd | grep ^kas | sed 's/^kas //g' | grep cp >AbilityData.slk.cook
cat $cmd | grep ^kas | sed 's/^kas //g' | grep -v cp >>AbilityData.slk.cook
../bin/prslk.py AbilityData.slk AbilityData.slk.cook >./data/AbilityData.slk

cp -f ./data/* /root/otg_game/uwin/.
