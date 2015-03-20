#!/bin/sh
appmf="app.manifest"
[ -e "$appmf.test" ] || mv $appmf "$appmf.test"
python main.py

