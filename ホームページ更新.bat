@echo off
setlocal enableextensions

rem Keep default code page to avoid locale-specific issues

rem Always run from this script directory
cd /d "%~dp0"

echo =========================================
echo Homepage update tool (v2026-05-12.2)
echo =========================================
echo Working directory: %CD%
echo.

if not exist "convert_data.py" (
    echo [ERROR] convert_data.py was not found in: %CD%
    echo Put this .bat in the same folder as convert_data.py and run it again.
    pause
    exit /b 1
)

echo [1/2] Running data conversion...
python "%CD%\convert_data.py"
if errorlevel 1 (
    echo [ERROR] Data conversion failed.
    pause
    exit /b 1
)
echo [OK] Data conversion finished.
echo.

echo [2/2] Uploading changes to GitHub...

rem Token source priority:
rem   1) GITHUB_TOKEN environment variable
rem   2) token file: github_token.txt (same folder as this .bat)
set "TOKEN_FILE=%CD%\github_token.txt"
if not defined GITHUB_TOKEN (
    if not exist "%TOKEN_FILE%" (
        echo [ERROR] Token not found.
        echo Set GITHUB_TOKEN or create github_token.txt next to this script.
        pause
        exit /b 1
    )
    set /p GITHUB_TOKEN=<"%TOKEN_FILE%"
)

if not defined GITHUB_TOKEN (
    echo [ERROR] Token is empty.
    pause
    exit /b 1
)

git add .
git commit -m "Auto-update website contents via batch file"
if errorlevel 1 (
    echo [ERROR] Commit failed (possibly no changes).
    pause
    exit /b 1
)

git push https://%GITHUB_TOKEN%@github.com/shibulab42/_MRI.git
if errorlevel 1 (
    echo [ERROR] Push failed.
    pause
    exit /b 1
)

echo.
echo =========================================
echo Update completed.
echo Reload your site after a few minutes.
echo =========================================
pause