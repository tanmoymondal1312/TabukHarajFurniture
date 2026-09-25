@echo off
cd /d "%~dp0"
echo Starting Django on http://0.0.0.0:8000
echo Genymotion device URL: http://192.168.56.2:8000
python manage.py runserver 0.0.0.0:8000
pause
