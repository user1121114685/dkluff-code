#!/bin/sh
# $1 $2 $3 $4
# srcdir orgname newname stringna

rblock(){
  cat $1 | sed -e '/./{H;$!d;}' -e "x;/$2/b" -e d
}
