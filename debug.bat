@echo off
echo Running PyQt5 diagnostic test...
cd windows-app
python debug_test.py > debug_output.txt 2>&1
echo Result code: %errorlevel%
echo.
echo Debug output:
type debug_output.txt
echo.
echo Checking PyQt5 installation...
pip show PyQt5
echo.
echo Done.
pause
