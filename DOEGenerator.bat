@echo off

set DUH_BIN=%~dp0

set PYTHON=python
set PYTHONPATH=%DUH_BIN%

for /f %%a in ('type "%DUH_BIN%\PythonEnvironment.txt"') do set PYTHON=%%a

%PYTHON% %DUH_BIN%\Backbone\DOEGenerator.py %1 %2 %3 %4 %5 %6 %7 %8 %9

