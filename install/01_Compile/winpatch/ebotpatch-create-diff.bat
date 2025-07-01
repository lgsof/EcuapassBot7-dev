REM Generate a patch file (path-YYYYMMDDHHMM.vcdiff) comparing the old and new EXE.

@echo off
for /f "tokens=2 delims==" %%G in ('wmic os get localdatetime /value') do set datetime=%%G
set DATETIME=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%-%datetime:~8,2%%datetime:~10,2%
echo %DATETIME%

set PATCHFILENAME=patch_%DATETIME%.vcdiff

xdelta3 -ef -s ecuapass_commander-ORG-Jun27.exe ecuapass_commander-NEW.exe %PATCHFILENAME%

del patches\patch*
copy %PATCHFILENAME% patches

