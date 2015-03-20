appmf="app.manifest"
[ -e $appmf ] || mv "$appmf.test" $appmf
sed -i '$d' $appmf
echo "#`date`" >> $appmf
python main.py
