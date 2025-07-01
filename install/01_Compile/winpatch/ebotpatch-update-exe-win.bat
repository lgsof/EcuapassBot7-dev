@echo off
setlocal enabledelayedexpansion

:: File paths
set "LOG_FILE=patches.log"
set "CURRENT_EXE=..\ecuapass_commander\ecuapass_commander.exe"
set "ORIGINAL_EXE=..\ecuapass_commander\ecuapass_commander_original.exe"
set "NEW_EXE=..\ecuapass_commander\new_ecuapass_commander.exe"

cd /d "%~dp0"

REM Check/Create log file 
if not exist "%LOG_FILE%" type nul > "%LOG_FILE%"

REM Ensure original exe file exists
if not exist "%ORIGINAL_EXE%" (
    echo +++ Creating original backup: %ORIGINAL_EXE%
    copy "%CURRENT_EXE%" "%ORIGINAL_EXE%" >nul || (
        echo !!! ERROR: Failed to create backup. Aborting.
        goto end
    )
)

REM Find the single patch file (e.g., patch_001.vcdiff)
set "PATCH_FILE="
for /f "delims=" %%F in ('dir /b patch_*.vcdiff 2^>nul') do set "PATCH_FILE=%%F"

if not defined PATCH_FILE (
    echo !!! No patch file found. Expected patch_*.vcdiff.
    goto end
)

REM Extract version using SPLIT (more reliable than string slicing)
for /f "tokens=2 delims=_" %%V in ("%PATCH_FILE%") do (
    for /f "tokens=1 delims=." %%N in ("%%V") do (
        set "PATCH_VERSION=%%N"
    )
)

if not defined PATCH_VERSION (
    echo !!! ERROR: Could not parse version from %PATCH_FILE%.
    goto end
)

REM Check if already applied
findstr /C:"%PATCH_VERSION%" "%LOG_FILE%" >nul && (
    echo --- Ultimo parche aplicado: %PATCH_VERSION%.
    goto end
)

REM Apply patch %PATCH_FILE%...
xdelta3.exe -f -d -s "%ORIGINAL_EXE%" "%PATCH_FILE%" "%NEW_EXE%"

if not exist "%NEW_EXE%" (
    echo !!! ERROR: Parche ha fallado--xdelta3 error--Aborting.
    goto end
)

REM Borrando parche y archivo actualizado
del "%CURRENT_EXE%" && (
    move "%NEW_EXE%" "%CURRENT_EXE%" >nul || (
        echo !!! ERROR: Failed to replace EXE. Restore from backup if needed.
        goto end
    )
)

del PATCH_FILE

REM Prepend to log file (newest first)
echo %PATCH_VERSION% > temp.log
type "%LOG_FILE%" >> temp.log
move /y temp.log "%LOG_FILE%" >nul
echo +++ Parche %PATCH_VERSION% aplicado exitosamente.

:end
