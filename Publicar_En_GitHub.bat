@echo off
chcp 65001 >nul
title Publicar Dashboard en GitHub Pages
cd /d "%~dp0"
echo ========================================================
echo       SALESLAND | Publicar en GitHub Pages (24/7)
echo ========================================================
echo.
echo 1. Si aun no has creado el repositorio en GitHub:
echo    Entra a: https://github.com/new
echo    Crea un repositorio publico (ej: salesland-dashboard)
echo.
echo 2. Pega aqui la URL de tu repositorio de GitHub:
echo    (Ejemplo: https://github.com/tu-usuario/salesland-dashboard.git)
echo.
set /p REPO_URL="Pega tu enlace de GitHub: "

if "%REPO_URL%"=="" (
    echo No ingresaste ninguna URL.
    pause
    exit /b
)

git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
echo.
echo Subiendo archivos a GitHub...
git push -u origin main

echo.
echo ========================================================
echo Subida completada con exito.
echo.
echo Para que quede activo 24/7 de forma permanente:
echo 1. En tu GitHub, ve a la pestaña "Settings"
echo 2. En el menu izquierdo haz clic en "Pages"
echo 3. En "Branch", selecciona "main" y haz clic en "Save".
echo.
echo En 30 segundos tu enlace fijo estara activo en:
echo https://[tu-usuario].github.io/salesland-dashboard/
echo ========================================================
pause
