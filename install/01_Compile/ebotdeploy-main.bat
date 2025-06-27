REM Create windows executable with dependencies
REM Create windir with pyc files and run pyinstaller 

REM remove OLD dir and rename current to OLD
rmdir /s /q winexe-OLD >nul 2>&1
ren winexe winexe-OLD >nul 2>&1

REM build exe dir
python ebotdeploy-build.py

REM Run pyinstaller in new dir
cd winexe
pyinstaller ebotdeploy-pyinstaller.spec

REM Create patch as 'patch-NEW.vcdiff'
cd ..
cd winpatch
ebotpatch-create-diff.bat


