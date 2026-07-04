import pytest
from src.utils.seguridad import (
    encriptar_dato,
    desencriptar_dato,
    encriptar_contrasena,
    verificar_contrasena,
)


class TestCifradoFernet:
    def test_round_trip(self):
        original = "Hola mundo"
        cifrado = encriptar_dato(original)
        descifrado = desencriptar_dato(cifrado)
        assert descifrado == original

    def test_vacio_retorna_vacio(self):
        assert encriptar_dato("") == ""
        assert desencriptar_dato("") == ""

    def test_texto_largo(self):
        original = "a" * 1000
        assert desencriptar_dato(encriptar_dato(original)) == original

    def test_caracteres_especiales(self):
        original = "ñáéíóúüÑ€®™☺✓🔥"
        assert desencriptar_dato(encriptar_dato(original)) == original


class TestHashingContrasena:
    def test_hash_consistente(self):
        h1 = encriptar_contrasena("admin123")
        h2 = encriptar_contrasena("admin123")
        assert h1 == h2

    def test_hash_diferente_para_distintas_contrasenas(self):
        h1 = encriptar_contrasena("pass1")
        h2 = encriptar_contrasena("pass2")
        assert h1 != h2

    def test_verificar_exitoso(self):
        h = encriptar_contrasena("mi_clave")
        assert verificar_contrasena("mi_clave", h) is True

    def test_verificar_fallido(self):
        h = encriptar_contrasena("clave_correcta")
        assert verificar_contrasena("clave_incorrecta", h) is False

    def test_verificar_vacio(self):
        h = encriptar_contrasena("")
        assert verificar_contrasena("", h) is True
