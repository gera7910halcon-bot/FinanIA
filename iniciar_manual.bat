@echo off
setlocal
REM Script robusto para iniciar el servidor FinanIA
REM Crea/activa .venv, instala dependencias y arranca app.py

echo.
echo ========================================
echo    INICIO DEL SERVIDOR FINANIA
echo ========================================
echo.
echo Preparando entorno...
echo.

REM 1) Buscar launcher Python
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PY_CMD=python"
    ) else (
        echo [ERROR] No se encontro Python ni el launcher "py".
        echo Instala Python y vuelve a ejecutar este script.
        pause
        exit /b 1
    )
)

REM 2) Crear venv si no existe
if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual .venv...
    %PY_CMD% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

REM 3) Activar entorno virtual
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

REM 4) Instalar dependencias
if exist "requirements.txt" (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Fallo al instalar dependencias.
        pause
        exit /b 1
    )
)

REM 5) Iniciar servidor
echo.
echo Iniciando servidor en http://localhost:5000
echo Presiona Ctrl+C para detenerlo.
echo.
"%CD%\.venv\Scripts\python.exe" app.py

if errorlevel 1 (
    echo.
    echo [ERROR] El servidor finalizo con error.
    pause
    exit /b 1
)

endlocal


