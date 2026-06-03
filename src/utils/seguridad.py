import os
import base64
from hashlib import sha256
from cryptography.fernet import Fernet

def _generar_clave_consistente():
    try:
        usuario_sistema = os.getlogin()
    except Exception:
        usuario_sistema = "clave_de_respaldo_segura_sistema_inventario"
        
    hash_usuario = sha256(usuario_sistema.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hash_usuario)

_clave_maestra = _generar_clave_consistente()
_suite_cifrado = Fernet(_clave_maestra)

def encriptar_contrasena(contrasena: str) -> str:
    if not contrasena:
        return ""
    return sha256(contrasena.encode('utf-8')).hexdigest()

def verificar_contrasena(contrasena_plana: str, contrasena_encriptada: str) -> bool:
    return encriptar_contrasena(contrasena_plana) == contrasena_encriptada

def encriptar_dato(texto: str) -> str:
    if not texto:
        return ""
    try:
        return _suite_cifrado.encrypt(texto.encode('utf-8')).decode('utf-8')
    except Exception:
        return ""

def desencriptar_dato(texto_encriptado: str) -> str:
    if not texto_encriptado:
        return ""
    try:
        return _suite_cifrado.decrypt(texto_encriptado.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[Error de Cifrado / Archivo Alterado]"