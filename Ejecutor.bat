@echo off
cd /d "C:\Users\User\Desktop\ProyectoKyklos\reciclaje"
start python manage.py runserver 0.0.0.0:8000
start "" "http://192.168.4.242:8000"
pause
