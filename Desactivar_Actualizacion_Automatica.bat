@echo off
chcp 65001 >nul
title Desactivar Actualizacion Automatica
echo ======================================================================
echo     SALESLAND | Desactivar Tareas Programadas de Actualizacion
echo ======================================================================
echo.
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate" /f >nul 2>&1
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate_08" /f >nul 2>&1
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate_12" /f >nul 2>&1
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate_16" /f >nul 2>&1
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate_18" /f >nul 2>&1
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate_20" /f >nul 2>&1
echo Todas las tareas automaticas de actualizacion han sido eliminadas.
echo.
pause
