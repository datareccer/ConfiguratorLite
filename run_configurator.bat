@echo off
call %~dp0\.venv\Scripts\activate
python src\configurator_lite.py %*
