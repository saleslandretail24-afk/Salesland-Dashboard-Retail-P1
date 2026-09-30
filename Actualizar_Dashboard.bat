@echo off
chcp 65001 >nul
title Actualizar Dashboard Salesland desde Excels
cd /d "C:\Users\Lenovo\Documents\Mi dashboard"
cls
echo ======================================================================
echo          SALESLAND ^| Retail - Actualizador Automático de Dashboard
echo ======================================================================
echo.
echo [1/3] Leyendo "Dashboard HTML RETAIL .xlsx" y "Dashboard HTML PREPAGO.xlsx"...
echo       Extrayendo ventas, calculando Pospago consolidado y metas...
echo.
python actualizar_datos.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Hubo un inconveniente al procesar los archivos Excel.
    echo Verifica que los archivos no esten bloqueados por otro programa.
    echo.
    pause
    exit /b
)
echo.
echo ======================================================================
echo       ¡DASHBOARD ACTUALIZADO Y PUBLICADO CON ÉXITO!
echo ======================================================================
echo.
echo Puedes ver los datos actualizados de inmediato en:
echo.
echo -> Tu computadora (Local):
echo    http://localhost:8080/index.html
echo.
echo -> Enlace en la Nube (GitHub Pages):
echo    https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/
echo.
echo ======================================================================
echo La ventana se cerrara automaticamente en 10 segundos...
timeout /t 10
