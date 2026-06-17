@echo off
title Wiring for Dummies
cd /d "%~dp0"
cls

echo.
echo   ^>^>^> WIRING FOR DUMMIES ^<^<^<
echo.
echo   Checking environment...

:: Kill any existing process on port 3000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000 " ^| findstr LISTENING') do (
    echo   Port 3000 in use — stopping PID %%a
    taskkill /f /pid %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

:: Try uv first — install if missing
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo   uv not found. Attempting install...

    :: Method 1: winget
    where winget >nul 2>nul
    if %errorlevel% equ 0 (
        echo   Trying winget...
        winget install --id=astral.uv --silent --accept-package-agreements >nul 2>&1
        if %errorlevel% equ 0 goto :uv_ready
    )

    :: Method 2: PowerShell iex (official install script)
    where powershell >nul 2>nul
    if %errorlevel% equ 0 (
        echo   Trying official install script...
        powershell -NoProfile -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; irm https://astral.sh/uv/install.ps1 | iex}" >nul 2>&1
        if %errorlevel% equ 0 (
            :: Add uv to PATH for this session if installed to ~/.cargo/bin
            for /f "delims=" %%i in ('powershell -NoProfile -Command "[System.Environment]::GetFolderPath('UserProfile')"') do set "UV_DIR=%%i\.cargo\bin"
            if exist "%UV_DIR%\uv.exe" set "PATH=%UV_DIR%;%PATH%"
            where uv >nul 2>nul
            if %errorlevel% equ 0 goto :uv_ready
        )
    )

    :: Method 3: pip (fallback)
    echo   Trying pip...
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        py -m pip install uv -q
    ) else if exist "C:\Python314\python.exe" (
        C:\Python314\python.exe -m pip install uv -q
    ) else if exist "C:\Python313\python.exe" (
        C:\Python313\python.exe -m pip install uv -q
    ) else if exist "C:\Python312\python.exe" (
        C:\Python312\python.exe -m pip install uv -q
    ) else (
        echo   [!] All install methods failed and Python not found.
        goto :fallback_py
    )
    where uv >nul 2>nul
    if %errorlevel% neq 0 (
        echo   [!] uv install failed. Falling back to direct Python.
        goto :fallback_py
    )
)

:uv_ready
echo   Found: uv
echo   Syncing environment...
call uv sync >nul 2>&1
echo.
echo   Server starting at http://localhost:3000
echo   Press Ctrl+C to stop
echo.
uv run main.py
goto :end

:: Fallback: find Python directly
:fallback_py
echo.
echo   Locating Python...
where py >nul 2>nul
if %errorlevel% equ 0 goto :run_py

if exist "C:\Python314\python.exe" set PYCMD=C:\Python314\python.exe & goto :run
if exist "C:\Python313\python.exe" set PYCMD=C:\Python313\python.exe & goto :run
if exist "C:\Python312\python.exe" set PYCMD=C:\Python312\python.exe & goto :run

echo   [!] Python not found.
echo.
echo   Options:
echo     npx http-server .   (if Node.js is installed)
echo     python main.py      (if Python is in your PATH)
echo.
pause
exit /b

:run_py
echo   Found: py (Python Launcher)
echo.
echo   Server starting at http://localhost:3000
echo   Press Ctrl+C to stop
echo.
py main.py
goto :end

:run
echo   Found: %PYCMD%
echo.
echo   Server starting at http://localhost:3000
echo   Press Ctrl+C to stop
echo.
%PYCMD% main.py
goto :end

:end
echo.
echo   Server stopped.
pause
