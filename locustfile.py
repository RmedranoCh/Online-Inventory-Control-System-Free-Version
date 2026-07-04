from locust import HttpUser, task, between


class InventoryUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.producto_count = 0

    @task(5)
    def ver_pagina_principal(self):
        self.client.get("/")

    @task(2)
    def exportar_excel(self):
        self.producto_count += 1
        payload = {
            "productos": [
                {
                    "nombre": f"Producto Carga {self.producto_count}",
                    "cantidad": 50,
                    "precio_costo": 250.0,
                    "stock_minimo": 5,
                    "detalles": "Test de carga",
                }
            ],
            "historial": [
                {
                    "fecha": "2024-06-01 10:00:00",
                    "tipo": "CREACION",
                    "descripcion": "Ingreso: Producto Carga | Cantidad: 50 uds | Costo Unitario: $250",
                }
            ],
            "excel_count": 0,
        }
        self.client.post("/api/excel", json=payload)
