import os
import base64
from hashlib import sha256
from cryptography.fernet import Fernet

_CLAVE_MAESTRA = None

def _obtener_clave():
    global _CLAVE_MAESTRA
    if _CLAVE_MAESTRA is None:
        clave = os.environ.get("INVENTORY_SECRET_KEY")
        if not clave:
            clave = "clave_segura_defecto_sistema_inventario_2024"
        hash_clave = sha256(clave.encode("utf-8")).digest()
        _CLAVE_MAESTRA = base64.urlsafe_b64encode(hash_clave)
    return _CLAVE_MAESTRA

def _obtener_suite():
    return Fernet(_obtener_clave())

def encriptar_dato(texto: str) -> str:
    if not texto:
        return ""
    try:
        return _obtener_suite().encrypt(texto.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""

def desencriptar_dato(texto_encriptado: str) -> str:
    if not texto_encriptado:
        return ""
    try:
        return _obtener_suite().decrypt(texto_encriptado.encode("utf-8")).decode("utf-8")
    except Exception:
        return "[Error de Cifrado / Archivo Alterado]"

def encriptar_contrasena(contrasena: str) -> str:
    return sha256(contrasena.encode("utf-8")).hexdigest()

def verificar_contrasena(contrasena: str, hash_almacenado: str) -> bool:
    return encriptar_contrasena(contrasena) == hash_almacenado
