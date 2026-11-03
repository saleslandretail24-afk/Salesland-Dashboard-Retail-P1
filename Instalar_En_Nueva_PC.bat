@echo off
chcp 65001 >nul
title Instalador Automatico - Salesland Dashboard Retail (P1 y P2)
cd /d "%~dp0"
cls
echo ======================================================================
echo     SALESLAND ^| Retail - Instalador Portatil para Nueva Computadora
echo ======================================================================
echo.
echo [1/4] Verificando entorno de Python y librerias (pandas, openpyxl)...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Python no se detecto en el PATH. Si vas a procesar archivos Excel
    echo         locales, instala Python 3.10+ desde https://www.python.org/
) else (
    pip install pandas openpyxl --quiet
    echo [OK] Python y librerias Excel listas.
)

echo.
echo [2/4] Verificando Node.js para servidor local en vivo...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Node.js no se detecto. Instala Node.js desde https://nodejs.org/
    echo         para usar el servidor en vivo (puerto 8080).
) else (
    echo [OK] Node.js detectado correctamente.
)

echo.
echo [3/4] Sincronizando copia espejo dashboard.html...
if exist "index.html" (
    copy /Y "index.html" "dashboard.html" >nul
    echo [OK] dashboard.html sincronizado con index.html.
)

echo.
echo [4/4] Creando acceso directo en el Escritorio...
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Salesland Dashboard Retail.lnk'); $s.TargetPath = '%~dp0Abrir_Dashboard.bat'; $s.WorkingDirectory = '%~dp0'; $s.Save()" >nul 2>&1
echo [OK] Acceso directo 'Salesland Dashboard Retail' creado en el Escritorio.

echo.
echo ======================================================================
echo       ¡INSTALACION COMPLETADA CON EXITO EN ESTA COMPUTADORA!
echo ======================================================================
echo.
echo Pasos opcionales:
echo  - Coloca tus 3 archivos Excel en esta carpeta:
echo      1. Dashboard HTML RETAIL .xlsx
echo      2. Dashboard HTML PREPAGO.xlsx
echo      3. RETAIL P2.xlsx
echo  - Haz doble clic en 'Abrir_Dashboard.bat' o en el icono del Escritorio.
echo.
pause
