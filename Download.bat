@echo off
setlocal

:: Define the URL for your Python script
set "PYTHON_SCRIPT_URL=https://raw.githubusercontent.com/GABYSYS1/GABYSYS1/main/Start.py"
set "PYTHON_SCRIPT_NAME=start.py"

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer
    bitsadmin /transfer "PythonInstaller" https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe "%temp%\python-installer.exe"

    :: Install Python silently with pip and add to PATH
    "%temp%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    if %errorlevel% neq 0 (
        echo Failed to install Python. Please install it manually and rerun this script.
        pause
        exit /b
    )
) else (
    echo Python is already installed.
)

:: Ensure pip is installed and updated
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: List of required Python packages
set "packages=requests beautifulsoup4 selenium webdriver-manager psutil colorama python-docx"

:: Install each package
for %%p in (%packages%) do (
    echo Installing Python package %%p...
    python -m pip install %%p --quiet
    if %errorlevel% neq 0 (
        echo Failed to install Python package %%p. Please check your internet connection or package name.
        pause
        exit /b
    )
)

:: Download the Python script from your GitHub repository
echo Downloading %PYTHON_SCRIPT_NAME% from GitHub...
curl -L -o %PYTHON_SCRIPT_NAME% %PYTHON_SCRIPT_URL%

if %errorlevel% neq 0 (
    echo Failed to download %PYTHON_SCRIPT_NAME%. Please check your internet connection and the URL.
    pause
    exit /b
)

:: Clear the screen to reset the chat
cls

:: Run the Python script after installing everything
echo Running %PYTHON_SCRIPT_NAME%...
python %PYTHON_SCRIPT_NAME%

echo All done!
pause
endlocal
