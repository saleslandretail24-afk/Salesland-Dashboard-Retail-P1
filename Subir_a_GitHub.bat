@echo off
chcp 65001 >nul
title Subir Dashboard a GitHub
cd /d "C:\Users\Lenovo\Documents\salesland-dashboard-web"
echo ========================================================
echo       SALESLAND | Subiendo Dashboard a GitHub
echo       Repositorio: Salesland-Dashboard-Retail-P1
echo ========================================================
echo.
echo Subiendo archivos (index.html, datos, etc.)...
echo Si te pide iniciar sesion, pulsa "Sign in with your browser".
echo.
git push -u origin main
echo.
echo ========================================================
if %ERRORLEVEL% EQU 0 (
    echo ¡SUBIDA COMPLETADA CON ÉXITO!
    echo.
    echo Pasos finales para activar tu enlace permanente 24/7:
    echo 1. Abre tu repositorio: https://github.com/saleslandretail24-afk/Salesland-Dashboard-Retail-P1
    echo 2. Haz clic en "Settings" (Configuracion) arriba a la derecha.
    echo 3. En el menu izquierdo haz clic en "Pages".
    echo 4. En "Branch" cambia None por "main" y haz clic en "Save".
    echo.
    echo En 1 minuto tu dashboard estara activo en:
    echo https://saleslandretail24-afk.github.io/Salesland-Dashboard-Retail-P1/
) else (
    echo Hubo un inconveniente al conectar con GitHub.
)
echo ========================================================
pause
