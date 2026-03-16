@echo off
color 0B
echo ==================================================
echo      REV'S BUTLER - PRODUCTION SUITE (v1.0)
echo ==================================================
echo.

:: Check if the executables exist before trying to run them
if not exist "dist\TechHaven_Dashboard\TechHaven_Dashboard.exe" (
    echo [ERROR] Dashboard executable not found in dist folder!
    pause
    exit
)

echo [1/2] Launching Dashboard Interface...
:: Start the compiled Flask EXE
start "TechHaven Dashboard" "dist\TechHaven_Dashboard\TechHaven_Dashboard.exe"

echo [2/2] Launching AI Bot Logic...
:: Start the compiled Bot EXE
start "Rev's Butler AI" "dist\Revs_Butler_Bot\Revs_Butler_Bot.exe"

echo.
echo --------------------------------------------------
echo Status: Executables deployed successfully.
echo Dashboard: http://127.0.0.1:5000
echo --------------------------------------------------
echo.
echo Keep this window open during the demo.
pause