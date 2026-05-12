@echo off
setlocal enableextensions

rem Keep default code page to avoid locale-specific issues

rem Always run from this script directory
cd /d "%~dp0"

echo =========================================
echo Homepage update tool (v2026-05-12.3)
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

echo [2/2] Committing and uploading changes to GitHub...

git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Auto-update website contents via batch file"
    if errorlevel 1 (
        echo [ERROR] Commit failed.
        pause
        exit /b 1
    )
) else (
    echo [INFO] No file changes detected. Skipping commit.
)

git push origin main
if errorlevel 1 (
    echo [ERROR] Push failed.
    echo If authentication is needed, run: gh auth login
    pause
    exit /b 1
)

echo.
echo =========================================
echo Update completed.
echo Reload your site after a few minutes.
echo =========================================
pause