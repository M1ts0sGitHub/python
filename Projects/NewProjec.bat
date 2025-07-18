echo off
cls
title Create Python Project
md NewProject
cd NewProject
python -m venv .venv
cd .venv
cd Scripts
type nul > App.py
echo python -m pip install --upgrade pip >> activate.bat
echo python -m pip list >> activate.bat
start activate.bat
start notepad ../../App.py