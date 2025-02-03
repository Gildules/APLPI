@echo off
REM Определяем корневую папку (папку, где находится сам скрипт)
set ROOT_DIR=%~dp0

REM Активируем виртуальное окружение
call "%ROOT_DIR%Jupyter/dist/ms_reader/Scripts/activate" 2>error_log.txt
if errorlevel 1 (
    echo Ошибка при активации виртуального окружения.
    pause
    exit /b 1
)

REM Переходим в папку проекта
cd "%ROOT_DIR%Jupyter/projects/File_converter" 2>>error_log.txt
if errorlevel 1 (
    echo Ошибка при переходе в папку проекта.
    pause
    exit /b 1
)

REM Запускаем main.py
cmd /k python main.py 2>>error_log.txt
if errorlevel 1 (
    echo Ошибка при выполнении main.py.
    pause
    exit /b 1
)

REM Ожидаем нажатия клавиши перед закрытием окна
pause
