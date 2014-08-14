#!/bin/bash

find $1  -type f   -exec mv  --backu="t" '{}' $2/dkspics.jpg \;

for f in `find $2 -type f`;do
mv $f $2/`md5sum $f | awk '{print $1}'`.jpg
done

find ~/aupic/new/ -type f -exec  ls {} -ltr \; | awk '{print $NF}' >flist.txt
