@echo off
start cmd /k "cd /d %~dp0 && cd ./src/ && title New CMD in Script Location && activate autogui"
