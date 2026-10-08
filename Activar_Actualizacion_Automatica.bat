@echo off
chcp 65001 >nul
title Configurar Actualizacion Automatica de Dashboard Salesland
echo ======================================================================
echo     SALESLAND ^| Retail - Programador de Actualizaciones Automaticas
echo ======================================================================
echo.
echo Este script configurara una Tarea Programada en Windows para que
echo el Dashboard se actualice automaticamente desde los archivos Excel
echo y se publique de inmediato en GitHub Pages a las horas seleccionadas.
echo.
echo La ejecucion es 100%% silenciosa (en segundo plano sin ventanas emergentes).
echo.
echo ======================================================================
echo Selecciona la frecuencia deseada:
echo ======================================================================
echo  [1] Cada 1 hora (durante todo el dia)
echo  [2] Cada 2 horas (durante todo el dia)
echo  [3] 4 veces al dia (8:00 AM, 12:00 PM, 4:00 PM y 8:00 PM)
echo  [4] 2 veces al dia (8:00 AM y 6:00 PM)
echo  [5] Cancelar
echo ======================================================================
set /p OPCION="Ingresa tu opcion (1-5): "

if "%OPCION%"=="1" goto CADA_1_HORA
if "%OPCION%"=="2" goto CADA_2_HORAS
if "%OPCION%"=="3" goto CUATRO_VECES
if "%OPCION%"=="4" goto DOS_VECES
if "%OPCION%"=="5" goto FIN

:CADA_1_HORA
echo.
echo Configurando actualizacion cada 1 hora...
schtasks /create /tn "Salesland_Dashboard_AutoUpdate" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc hourly /mo 1 /f
goto FINALIZADO

:CADA_2_HORAS
echo.
echo Configurando actualizacion cada 2 horas...
schtasks /create /tn "Salesland_Dashboard_AutoUpdate" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc hourly /mo 2 /f
goto FINALIZADO

:CUATRO_VECES
echo.
echo Configurando actualizacion 4 veces al dia (08:00, 12:00, 16:00, 20:00)...
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate" /f >nul 2>&1
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_08" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 08:00 /f
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_12" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 12:00 /f
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_16" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 16:00 /f
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_20" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 20:00 /f
goto FINALIZADO

:DOS_VECES
echo.
echo Configurando actualizacion 2 veces al dia (08:00 y 18:00)...
schtasks /delete /tn "Salesland_Dashboard_AutoUpdate" /f >nul 2>&1
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_08" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 08:00 /f
schtasks /create /tn "Salesland_Dashboard_AutoUpdate_18" /tr "wscript.exe \"C:\Users\Lenovo\Documents\Mi dashboard\actualizar_silencioso.vbs\"" /sc daily /st 18:00 /f
goto FINALIZADO

:FINALIZADO
echo.
echo ======================================================================
echo ¡CONFIGURACION COMPLETADA CON EXITO!
echo Las tareas se ejecutaran de manera silenciosa en Windows.
echo Puedes verificar o modificar las tareas en cualquier momento.
echo ======================================================================
pause
exit /b

:FIN
echo Operacion cancelada.
exit /b
