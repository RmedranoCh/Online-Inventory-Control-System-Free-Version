import os
import sqlite3
import sys

def obtener_ruta_base_datos():
    if sys.platform == "win32":
        ruta_sistema = os.getenv("APPDATA")
    else:
        ruta_sistema = os.path.expanduser("~")
        
    carpeta_app = os.path.join(ruta_sistema, ".sistema_inventario_pro")
    
    os.makedirs(carpeta_app, exist_ok=True)
    
    return os.path.join(carpeta_app, "secure_data.db")

def obtener_conexion():
    ruta_db = obtener_ruta_base_datos()
    conexion = sqlite3.connect(ruta_db)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion