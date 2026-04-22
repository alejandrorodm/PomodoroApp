@echo off
setlocal
echo ========================================================
echo         COMPILADOR DE POMODORO GIRLY - MODO PRO
echo ========================================================

:: 1. Limpieza de carpetas de compilación (esto sí es necesario)
echo [1/5] Limpiando archivos temporales de PyInstaller...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del /q *.spec 2>nul

:: 2. Activar tu venv existente
echo [2/5] Activando tu entorno virtual...
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo ERROR: No se encuentra la carpeta 'venv'. Asegurate de estar en la raiz del proyecto.
    pause
    exit /b
)

:: 3. Asegurar dependencias críticas
echo [3/5] Verificando motor PySide6 (para evitar errores de DLL)...
pip install PySide6 pywebview pyinstaller --upgrade

:: 4. Convertir Icono (Solo si existe el PNG y no el ICO)
echo [4/5] Gestionando icono...
if exist "PomodoroAppIcono.png" (
    python make_icon.py
)

:: 5. Compilar usando el motor QT
echo [5/5] Compilando ejecutable...
:: Usamos --collect-all PySide6 para que no falte ni una sola pieza del motor grafico
:: Anadimos --clean para limpiar la cache, y cambiamos el nombre para burlar la cache de iconos de Windows
pyinstaller --noconfirm --clean --onefile --windowed ^
    --name "Pomodoro Power" ^
    --icon "PomodoroAppIcono.ico" ^
    --add-data "templates;templates" ^
    --add-data "frases_personalizadas.txt;." ^
    --collect-all webview ^
    desktop_app.py
echo.
echo ========================================================
echo ¡LISTO! Todo empaquetado en 'dist\Pomodoro girly'
echo ========================================================
pause