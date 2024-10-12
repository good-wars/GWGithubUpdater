@echo off

REM Проверка установлен ли PyInstaller
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller Ne Naiden. Idet Ustanovka
    pip install pyinstaller
) else (
    echo PyInstaller Uze Ustanovlen.
)

REM Компиляция приложения
echo Kompiliruem Prilozenie...
pyinstaller --noconfirm --onedir --windowed --add-data "C:/Users/AstroPowerX/AppData/Local/Programs/Python/Python312/Lib/site-packages/customtkinter;customtkinter/" "app.py"

echo Kompilyatia zavershena!
pause
