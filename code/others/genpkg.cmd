set PYTHONOPTIMIZE=1

copy /Y I:\Pirate\Docs\dkluffy_git\dkluff-code\code\others\*.py .

rem I:\anaconda2\Scripts\pyinstaller.exe -F -c --upx-dir=upx394 cookxls_pv1.py

rem I:\anaconda2\Scripts\pyinstaller.exe -c --noupx cookxls_pv1.py

I:\anaconda2\Scripts\pyinstaller.exe -y -c --noupx cookxls_pv1.spec


rem copy /Y I:\temp_del_anytime\debug_ota_py\toexe\build\cookxls_pv1\* I:\temp_del_anytime\debug_ota_py\toexe\sent\dist\cookxls_pv1\

copy /Y I:\temp_del_anytime\debug_ota_py\toexe\dist\cookxls_pv1\cookxls_pv1.exe I:\temp_del_anytime\debug_ota_py\toexe\sent\dist\cookxls_pv1\
pause