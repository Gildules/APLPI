@echo off

REM Enable extension in Jupyter Notebook.
REM Example:
REM enable_extension.bat widgetsnbextension

call %~dp0\setenv.bat
call %~dp0\pyenv3.7-win64\Scripts\jupyter-nbextension.exe enable %1