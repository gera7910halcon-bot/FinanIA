@echo off
setlocal
chcp 65001 >nul

cd /d "%~dp0"

set "LOG_FILE=%~dp0automatizar_finania.log"
set "KEEP_OPEN=1"

echo ================================================== > "%LOG_FILE%"
echo Inicio: %DATE% %TIME% >> "%LOG_FILE%"
echo Directorio: %CD% >> "%LOG_FILE%"
echo ================================================== >> "%LOG_FILE%"

echo.
echo ========================================
echo   FINANIA - AUTOMATIZACION COMPLETA
echo ========================================
echo.
echo Log: "%LOG_FILE%"
echo.
echo [INFO] Ejecuta este script desde terminal para ver todo:
echo        cmd /k automatizar_finania.bat
echo.

REM ---------- Configuracion editable ----------
set "DB_HOST=localhost"
set "DB_PORT=3306"
set "DB_USER=root"
set "DB_PASS="
set "DB_NAME=finania"
set "SQL_FILE=actualizar_base_datos.sql"
set "RUN_DB_MIGRATION=1"
REM -------------------------------------------

where py >nul 2>nul
if not errorlevel 1 set "PY_CMD=py"
if not defined PY_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)
if not defined PY_CMD (
    echo [ERROR] No se encontro Python ^(py/python^) en PATH.
    echo [ERROR] Python no encontrado. >> "%LOG_FILE%"
    goto :fail
)

echo [OK] Python detectado: %PY_CMD%
echo [OK] Python detectado: %PY_CMD% >> "%LOG_FILE%"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creando entorno virtual .venv...
    echo [INFO] Creando entorno virtual .venv... >> "%LOG_FILE%"
    %PY_CMD% -m venv .venv >> "%LOG_FILE%" 2>&1
    if errorlevel 1 goto :fail_venv
)

call ".venv\Scripts\activate.bat" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] No se pudo activar .venv.
    goto :fail
)
echo [OK] Entorno virtual activo.
echo [OK] Entorno virtual activo. >> "%LOG_FILE%"

if exist "requirements.txt" (
    echo [INFO] Instalando dependencias...
    echo [INFO] Instalando dependencias... >> "%LOG_FILE%"
    python -m pip install --upgrade pip >> "%LOG_FILE%" 2>&1
    pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
    if errorlevel 1 goto :fail_pip
)

if "%RUN_DB_MIGRATION%"=="1" (
    if exist "%SQL_FILE%" (
        where mysql >nul 2>nul
        if not errorlevel 1 (
            echo [INFO] Ejecutando SQL: %SQL_FILE%
            echo [INFO] Ejecutando SQL: %SQL_FILE% >> "%LOG_FILE%"
            if "%DB_PASS%"=="" goto :sql_without_pass
            goto :sql_with_pass
        ) else (
            echo [WARN] mysql no esta en PATH. Se omite migracion.
            echo [WARN] mysql no esta en PATH. >> "%LOG_FILE%"
        )
    )
)
goto :after_sql

:sql_without_pass
mysql -h %DB_HOST% -P %DB_PORT% -u %DB_USER% %DB_NAME% < "%SQL_FILE%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto :sql_warn
echo [OK] Migracion SQL aplicada.
goto :after_sql

:sql_with_pass
mysql -h %DB_HOST% -P %DB_PORT% -u %DB_USER% -p%DB_PASS% %DB_NAME% < "%SQL_FILE%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 goto :sql_warn
echo [OK] Migracion SQL aplicada.
goto :after_sql

:sql_warn
echo [WARN] Fallo migracion SQL. Revisa el log.
echo [WARN] Fallo migracion SQL. >> "%LOG_FILE%"

:after_sql
if not exist "app.py" (
    echo [ERROR] No se encontro app.py en %CD%
    goto :fail
)

echo.
echo ========================================
echo Iniciando servidor FinanIA...
echo URL: http://localhost:5000
echo Ctrl+C para detener
echo ========================================
echo.

start "" http://localhost:5000/
python app.py
if errorlevel 1 goto :fail_server

goto :success

:fail
echo.
echo Proceso finalizado con errores.
echo Revisa este archivo: "%LOG_FILE%"
echo.
pause
exit /b 1

:fail_venv
echo [ERROR] No se pudo crear .venv.
echo [ERROR] No se pudo crear .venv. >> "%LOG_FILE%"
goto :fail

:fail_pip
echo [ERROR] Fallo la instalacion de dependencias.
echo [ERROR] Fallo la instalacion de dependencias. >> "%LOG_FILE%"
goto :fail

:fail_server
echo [ERROR] El servidor se detuvo con error. Revisa el log.
echo [ERROR] El servidor se detuvo con error. >> "%LOG_FILE%"
goto :fail

:success
echo.
echo Proceso finalizado correctamente.
echo Log disponible en: "%LOG_FILE%"
echo.
pause
exit /b 0
