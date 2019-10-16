@echo off
set ScriptsPath="../Scripts/UI/"
echo %ScriptsPath%
for /f "delims=\" %%a in ('dir /b /a-d /o-d "%~dp0\*.ui"') do (
    echo %%a
    pyuic5 -o %ScriptsPath%%%~na.py %%a
)
pause