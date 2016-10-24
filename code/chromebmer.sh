#!/bin/sh
grep -v "chrome://bookmarks"|sed 's/^[ ]*//g' | grep  "<DT><A" | awk -F\< '{ print $3 }' | awk -F\" '
 BEGIN{
 print "<DL><p>"
 }
 {a[$2]=$NF} 
 END {

 for(k in a) print "<DT><A HREF=\""k"\""a[k]"</A>";
 print "</DL><p>"
 }'

#cat *.html | ./chromebmer.sh
