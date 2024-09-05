@echo off
:: Check if the script is running as Administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~0' -Verb RunAs"
    exit
)

:: Navigate to the folder where your script is located
cd /d "C:\Users\Andy\Documents\Programming\Python_Projects\a-dove-is-dumb"

:: Run the Python script
python main.py

:: Close the terminal when the script ends
exit
