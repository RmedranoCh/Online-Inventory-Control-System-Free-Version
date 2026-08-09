import pytest

from app import MAX_EXCEL, MAX_PRODUCTOS, app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestRutas:
    def test_index_devuelve_200(self, cliente):
        resp = cliente.get("/")
        assert resp.status_code == 200
        assert b"Control de Inventario" in resp.data


class TestExportarExcel:
    def test_excel_con_datos_validos(self, cliente):
        payload = {
            "productos": [{"nombre": "Test", "cantidad": 10, "precio_costo": 100.0, "stock_minimo": 2, "detalles": ""}],
            "historial": [],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 200
        assert resp.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def test_excel_sin_datos_devuelve_400(self, cliente):
        resp = cliente.post("/api/excel", json={})
        assert resp.status_code == 400
        assert b"Datos requeridos" in resp.data

    def test_excel_sin_productos_devuelve_400(self, cliente):
        resp = cliente.post("/api/excel", json={"productos": [], "historial": []})
        assert resp.status_code == 400
        assert b"No hay productos" in resp.data

    def test_excel_demasiados_productos_devuelve_400(self, cliente):
        payload = {
            "productos": [
                {"nombre": f"P{i}", "cantidad": 1, "precio_costo": 1.0, "stock_minimo": 1, "detalles": ""}
                for i in range(MAX_PRODUCTOS + 1)
            ],
            "historial": [],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 400
        assert b"Demasiados productos" in resp.data

    def test_excel_nombre_invalido_devuelve_400(self, cliente):
        payload = {
            "productos": [{"nombre": 123, "cantidad": 10, "precio_costo": 100.0, "stock_minimo": 2}],
            "historial": [],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 400

    def test_excel_valor_numerico_invalido_devuelve_400(self, cliente):
        payload = {
            "productos": [{"nombre": "Test", "cantidad": "diez", "precio_costo": 100.0, "stock_minimo": 2}],
            "historial": [],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 400

    def test_excel_limite_alcanzado_devuelve_403(self, cliente):
        payload = {
            "productos": [{"nombre": "Test", "cantidad": 10, "precio_costo": 100.0, "stock_minimo": 2, "detalles": ""}],
            "historial": [],
            "excel_count": MAX_EXCEL,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 403
        assert "Límite alcanzado" in resp.get_json()["error"]

    def test_excel_formato_invalido_devuelve_400(self, cliente):
        resp = cliente.post("/api/excel", json={"productos": "invalido", "historial": []})
        assert resp.status_code == 400
        assert "Formato inválido" in resp.get_json()["error"]


class TestHistorialYLimites:
    def test_historial_muy_largo_se_recorta(self, cliente):
        import app as modulo

        payload = {
            "productos": [{"nombre": "Test", "cantidad": 10, "precio_costo": 100.0, "stock_minimo": 2, "detalles": ""}],
            "historial": [
                {"fecha": "2024-01-01", "tipo": "CREACION", "descripcion": "x"}
                for _ in range(modulo.MAX_HISTORIAL + 10)
            ],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 200

    def test_historial_formato_invalido_devuelve_400(self, cliente):
        resp = cliente.post(
            "/api/excel",
            json={
                "productos": [{"nombre": "Test", "cantidad": 1, "precio_costo": 1.0, "stock_minimo": 1}],
                "historial": "mal",
                "excel_count": 0,
            },
        )
        assert resp.status_code == 400

    def test_excel_count_como_string_se_convierte(self, cliente):
        payload = {
            "productos": [{"nombre": "Test", "cantidad": 10, "precio_costo": 100.0, "stock_minimo": 2, "detalles": ""}],
            "historial": [],
            "excel_count": "0",
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 200

    def test_nombre_muy_largo_devuelve_400(self, cliente):
        payload = {
            "productos": [{"nombre": "x" * 501, "cantidad": 1, "precio_costo": 1.0, "stock_minimo": 1, "detalles": ""}],
            "historial": [],
            "excel_count": 0,
        }
        resp = cliente.post("/api/excel", json=payload)
        assert resp.status_code == 400


class TestSeguridadHeaders:
    def test_headers_seguridad_presentes(self, cliente):
        resp = cliente.get("/")
        assert resp.headers["X-Content-Type-Options"] == "nosniff"
        assert resp.headers["X-Frame-Options"] == "DENY"
        assert "default-src 'self'" in resp.headers["Content-Security-Policy"]
        assert resp.headers["Referrer-Policy"] == "no-referrer"
