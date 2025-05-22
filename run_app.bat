@echo off
cd /d %~dp0
echo Installing required packages...
python -m pip install PyQt5==5.15.10 selenium==4.18.1 webdriver-manager==4.0.1 Pillow==10.4.0
if %errorlevel% neq 0 (
    echo Failed to install packages.
    pause
    exit /b 1
)

echo.
echo Installation successful! Testing with simplified version...
echo.
cd windows-app
python simplified_main.py
if %errorlevel% neq 0 (
    echo.
    echo Test application exited with an error. Please check the error message above.
    echo.
    echo Let's try to run the full application...
    python main.py
) else (
    echo.
    echo Test successful! Now running the full application...
    python main.py
)
pause
