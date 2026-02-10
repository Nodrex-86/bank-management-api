@echo off
setlocal enabledelayedexpansion
echo [INFO] Collecting files for documentation...

:: Collect all .py files in the current directory
set "FILES="
for %%f in (*.py) do (
    set "FILES=!FILES! %%f"
)

:: Add the tests folder explicitly
set "FILES=!FILES! tests"

echo [INFO] Generating documentation for: %FILES%

:: Call pdoc with file paths
pdoc %FILES% -o ./dokumentation

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Documentation created in ./dokumentation.
) else (
    echo [ERROR] pdoc failed.
)
pause
