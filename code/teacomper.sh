#!/bin/bash
#brew install libgxps
#/usr/local/bin/pdfjoin -> /System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py
#/usr/local/bin/xpstopdf -> ../Cellar/libgxps/0.2.4/bin/xpstopdf
#brew install ImageMagick

outputdir=`pwd`
tmp_pdf1="$outputdir/$(date | md5 ).pdf"
#output="$outputdir/$(date | md5 )_output.pdf"
output="$1_output.pdf"

usage(){
  echo "Something wrong..."
  echo "Usage: $0 tea.xps 1.pdf 2.pdf"
  exit 0
}
[ $# -lt 1 ] && usage
[[ ! `echo $1 | grep -i xps$` ]] && usage

xpstopdf $1 $tmp_pdf1
shift

echo "pdfjoin --output $output $tmp_pdf1 $@"

#pdfjoin --output $output $tmp_pdf1 $@
#In this way will lost the chopper in pdf
convert -density 300 $tmp_pdf1 $@ $output
[ -f $tmp_pdf1 ] && rm -rf $tmp_pdf1
