import io
import openpyxl
import pytest
from src.utils.excel_exporter import generar_reporte_excel


class TestGenerarReporteExcel:
    def test_con_datos_devuelve_true(self):
        buffer = io.BytesIO()
        productos = [{"nombre": "Laptop", "cantidad": 10, "precio_costo": 500.0, "detalles": "", "stock_minimo": 2}]
        historial = [
            {"fecha": "2024-01-01 10:00", "tipo": "CREACION", "descripcion": "Ingreso: Laptop | Cantidad: 5 uds | Costo Unitario: $500"}
        ]
        assert generar_reporte_excel(buffer, productos, historial) is True

    def test_sin_productos_devuelve_true(self):
        buffer = io.BytesIO()
        assert generar_reporte_excel(buffer, [], []) is True

    def test_archivo_tiene_hojas_correctas(self):
        buffer = io.BytesIO()
        productos = [{"nombre": "Mouse", "cantidad": 20, "precio_costo": 15.0, "detalles": "", "stock_minimo": 5}]
        historial = []
        generar_reporte_excel(buffer, productos, historial)
        wb = openpyxl.load_workbook(buffer)
        assert "Libro Contable" in wb.sheetnames
        assert "Inventario Disponible" in wb.sheetnames

    def test_historial_con_varios_tipos(self):
        buffer = io.BytesIO()
        productos = [{"nombre": "Teclado", "cantidad": 8, "precio_costo": 30.0, "detalles": "", "stock_minimo": 3}]
        historial = [
            {"fecha": "2024-01-01", "tipo": "CREACION", "descripcion": "Ingreso: Teclado | Cantidad: 10 uds | Costo Unitario: $30"},
            {"fecha": "2024-01-02", "tipo": "VENTA", "descripcion": "Salida de stock | Cantidad: 2 uds | Precio Venta: $45 | Total: $90.00"},
            {"fecha": "2024-01-03", "tipo": "BAJO STOCK", "descripcion": "Stock bajo para: Teclado"},
        ]
        assert generar_reporte_excel(buffer, productos, historial) is True

    def test_multiples_productos(self):
        buffer = io.BytesIO()
        productos = [
            {"nombre": f"Producto {i}", "cantidad": i * 10, "precio_costo": float(i * 100), "detalles": "", "stock_minimo": 5}
            for i in range(1, 21)
        ]
        historial = []
        assert generar_reporte_excel(buffer, productos, historial) is True
