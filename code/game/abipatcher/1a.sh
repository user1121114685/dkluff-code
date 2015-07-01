cat mod.abicm.txt | sed -e '/./{H;$!d;}' -e "x;/$1/b;" -e d
