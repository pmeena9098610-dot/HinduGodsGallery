@echo off
chcp 65001 > nul
echo ===================================================================
echo ??? HINDU GODS GALLERY - AUTO DAILY UPDATE SETUP (Windows)
echo ===================================================================
echo.
echo ?? ????????? Windows Task Scheduler ??? ???-????? ????? ??????? ??????
echo ???? ??? ?? ??? ???? 06:00 ??? 10 ?? ????? ?? ???????? ??? ???????
echo.

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=python"

:: Test python existence
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python aapke computer me install nahi hai ya PATH me nahi hai!
    echo Kripya python install karein: https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Python check passed!
echo [2/3] Registering Task Scheduler job 'HinduGodsGalleryAutoDaily'...

schtasks /create /tn "HinduGodsGalleryAutoDaily" /tr "\"%PYTHON_EXE%\" \"%SCRIPT_DIR%auto_update.py\"" /sc daily /st 06:00 /f /rl HIGHEST

if %errorlevel% equ 0 (
    echo.
    echo ===================================================================
    echo ? SUCCESS! Task successfully registered!
    echo Har din subah 06:00 baje 10 naye bhagwan ke photo khud banenge!
    echo Aapko kuch bhi karne ki zaroorat nahi hai.
    echo ===================================================================
) else (
    echo [WARNING] Administrator rights chahiye ho sakte hain. Right click -> Run as Administrator karein.
)

echo.
echo Pehli baar test run karne ke liye koi bhi button dabayein...
pause > nul
python "%SCRIPT_DIR%auto_update.py"
pause
