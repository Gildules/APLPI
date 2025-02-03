@echo off

set conf_path=%~dp0conf

set JUPYTER_CONFIG_DIR=%conf_path%jupyter
set JUPYTER_DATA_DIR=%conf_path%jupyterdata
set JUPYTER_RUNTIME_DIR=%conf_path%jupyterdataruntime
set IPYTHONDIR=%conf_path%ipython
set MPLCONFIGDIR=%conf_path%matplotlib

REM Matplotlib search FFMPEG in PATH variable only!
set PATH=%~dp0appsffmpegbin;%PATH%