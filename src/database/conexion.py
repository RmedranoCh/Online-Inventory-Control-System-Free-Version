import os
import sqlite3

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

def obtener_ruta_base_datos():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    return os.path.join(CARPETA_DATOS, "web_data.db")

def obtener_conexion():
    ruta_db = obtener_ruta_base_datos()
    conexion = sqlite3.connect(ruta_db)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion
