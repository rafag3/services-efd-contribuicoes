@echo off
REM =========================================================
REM build.bat — Gera o executável EFD_Services.exe (Tkinter)
REM Requer Python + PyInstaller instalados
REM Executar na raiz do projeto: .\build.bat
REM =========================================================

echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Gerando executavel...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "EFD_Services" ^
  --hidden-import openpyxl ^
  --hidden-import pandas ^
  main.py

echo.
echo Concluido! Executavel em: dist\EFD_Services.exe
pause
