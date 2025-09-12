@echo off
python -m py_compile addon\globalPlugins\linky.py
if %errorlevel%==0 echo OK