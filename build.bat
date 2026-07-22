@echo off
echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo Gerando executavel...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "EFD_Services" ^
  --add-data "assets;assets" ^
  --hidden-import openpyxl ^
  --hidden-import pandas ^
  --hidden-import PIL ^
  main.py

echo.
echo Concluido! Executavel em: dist\EFD_Services.exe
pause
