@echo off
echo ========================================
echo ForensicCapture Tool - Launcher
echo ========================================
echo.

:menu
echo Please select an option:
echo 1. Install dependencies and run simplified test app
echo 2. Install dependencies and run full application
echo 3. Run application without installing dependencies
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto install_and_test
if "%choice%"=="2" goto install_and_run
if "%choice%"=="3" goto run_only
if "%choice%"=="4" goto end
echo Invalid choice. Please try again.
goto menu

:install_and_test
echo.
echo Installing required packages...
pip install PyQt5==5.15.10 selenium==4.18.1 webdriver-manager==4.0.1 Pillow==10.4.0
if %errorlevel% neq 0 (
    echo Failed to install packages.
    pause
    goto menu
)
echo.
echo Installation successful! Running simplified test application...
echo.
cd windows-app
python simplified_main.py
pause
goto menu

:install_and_run
echo.
echo Installing required packages...
pip install PyQt5==5.15.10 selenium==4.18.1 webdriver-manager==4.0.1 Pillow==10.4.0
if %errorlevel% neq 0 (
    echo Failed to install packages.
    pause
    goto menu
)
echo.
echo Installation successful! Running main application...
echo.
cd windows-app
python main.py
pause
goto menu

:run_only
echo.
echo Running main application without installing dependencies...
echo.
cd windows-app
python main.py
pause
goto menu

:end
echo.
echo Thank you for using ForensicCapture Tool!
echo.
echo ========================================
echo.
