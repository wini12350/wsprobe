@echo off
cd /d %~dp0
.venv\Scripts\python.exe -m wsprobe.scanner --url ws://127.0.0.1:8765 --token lab-token --output reports/wsprobe-report.json
pause
