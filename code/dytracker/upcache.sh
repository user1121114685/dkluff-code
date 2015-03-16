sed -i '$d' app.manifest
echo "#`date`" >> app.manifest
python main.py
