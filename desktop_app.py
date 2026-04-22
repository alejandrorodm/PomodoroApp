import sys
import os
import webview
from app import app as flask_app
import app as my_app_module

def get_bundle_path():
    """Ruta de los archivos empaquetados (templates, resources) read-only."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_exe_dir():
    """Ruta donde está ubicado el .exe para guardar datos persistentes."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Redirigir la ruta de los templates al paquete interno de PyInstaller
flask_app.template_folder = os.path.join(get_bundle_path(), 'templates')

# Mantener el archivo de frases dentro del empaquetado (solo lectura)
my_app_module.PHRASES_FILE = os.path.join(get_bundle_path(), 'frases_personalizadas.txt')

# Forzar que la base de datos (JSON) se guarde junto al .exe para que persista
my_app_module.DATA_FILE = os.path.join(get_exe_dir(), 'pomodoro_data.json')
my_app_module.TAGS_FILE = os.path.join(get_exe_dir(), 'pomodoro_tags.json')

if __name__ == '__main__':
    window = webview.create_window(
        'Pomodoro girly', 
        flask_app, 
        width=1000, 
        height=800,
        min_size=(600, 500)
    )
    
    webview.start()