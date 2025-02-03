@echo off

call %~dp0\setenv.bat
call %~dp0\pyenv3.7-win64\Scripts\jupyter-lab.exe --notebook-dir=%1