@echo off
setlocal
echo ========================================================
echo        CONFIGURADOR DE POMODORO GIRLY 2026
echo ========================================================

:: 1. Limpieza total
echo [1/6] Limpiando archivos temporales...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist venv rmdir /s /q venv
del /q *.spec 2>nul

:: 2. Crear Entorno Virtual (Garantiza que no falten librerias)
echo [2/6] Creando entorno virtual limpio...
python -m venv venv
call venv\Scripts\activate

:: 3. Instalar solo lo necesario
echo [3/6] Instalando dependencias en el entorno...
python -m pip install --upgrade pip
pip install pywebview pyinstaller Flask Pillow

:: 4. Convertir Icono
echo [4/6] Generando icono de aplicacion...
if exist "PomodoAppIcono.png" (
    python -c "from PIL import Image; img = Image.open('PomodoAppIcono.png'); img.save('PomodoAppIcono.ico', format='ICO', sizes=[(256, 256)])"
) else (
    echo AVISO: No se encontro PomodoAppIcono.png, se usara icono por defecto.
)

:: 5. Compilar con PyInstaller
echo [5/6] Compilando ejecutable (Motor: EdgeChromium)...
:: Nota: --collect-all webview asegura que se lleven todas las dependencias del motor web
pyinstaller --noconfirm --onedir --windowed ^
    --name "Pomodoro girly" ^
    --icon "PomodoAppIcono.ico" ^
    --add-data "templates;templates" ^
    --add-data "frases_personalizadas.txt;." ^
    --exclude-module "pythonnet" ^
    --exclude-module "clr" ^
    --collect-all webview ^
    desktop_app.py

echo.
echo ========================================================
echo [6/6] ¡PROCESO TERMINADO CON EXITO!
echo ========================================================
echo.
echo Pasos finales para que funcione en otros PCs:
echo 1. Ve a la carpeta 'dist\Pomodoro girly'
echo 2. NO envies solo el .exe, envia la CARPETA COMPLETA comprimida en un .zip
echo 3. El usuario debe descomprimir y ejecutar 'Pomodoro girly.exe'
echo.
pause