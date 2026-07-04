import pytest
from app import app, MAX_PRODUCTOS, MAX_EXCEL


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
            "productos": [{"nombre": f"P{i}", "cantidad": 1, "precio_costo": 1.0, "stock_minimo": 1, "detalles": ""} for i in range(MAX_PRODUCTOS + 1)],
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
        assert b"L\u00edmite alcanzado" in resp.data  # noqa: W605

    def test_excel_formato_invalido_devuelve_400(self, cliente):
        resp = cliente.post("/api/excel", json={"productos": "invalido", "historial": []})
        assert resp.status_code == 400
        assert b"Formato inv\u00e1lido" in resp.data  # noqa: W605
