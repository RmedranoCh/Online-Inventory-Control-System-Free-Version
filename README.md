# Sistema de Control de Inventario Online — Versión Gratuita

[![CI](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml/badge.svg)](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey)](https://flask.palletsprojects.com)

Aplicación web moderna para gestionar inventarios, registrar ventas y generar reportes contables en Excel. Construida con **Flask** en el backend y **HTML, CSS y JavaScript puro** en el frontend, sin frameworks ni librerías externas del lado del cliente.

Probada en vivo en: https://inventory-control-system-free.onrender.com

---

## Características

- **Sin registro, sin cuentas, sin correos**: todo se guarda en el navegador (`localStorage`). Tus datos se quedan contigo y nunca llegan a un servidor.
- **Gestión de productos**: agregar con nombre, cantidad, costo unitario, stock mínimo y detalles; editar o eliminar cuando quieras.
- **Registro de ventas** con descuento automático del stock.
- **Historial completo** de todo lo que ha pasado (altas, bajas, ventas, modificaciones).
- **Reporte contable en Excel** con dos hojas: libro contable (Kárdex) e inventario disponible, con fórmulas incluidas.
- **Límites validados en dos capas** (frontend y backend): máximo 20 productos y hasta 2 exportaciones de Excel por navegador. Pensado para demostración.

---

## Tecnologías

| Capa | Tecnología |
|------|------------|
| **Backend** | Python 3 + Flask |
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **Exportación** | openpyxl (Excel .xlsx) |
| **Seguridad** | cryptography (Fernet AES), SHA-256 |
| **Despliegue** | Gunicorn (Linux) / Waitress (Windows) |
| **CI/CD** | GitHub Actions (ruff + pyright) |
| **Tests** | pytest (32 tests) |
| **Carga** | Locust |

---

## Estructura del proyecto

```
inventory-control-system/
├── app.py                      # Servidor Flask con la API REST
├── server.py                   # Punto de entrada multiplataforma
├── run.py                      # Punto de entrada alternativo
├── templates/
│   └── index.html              # La aplicación completa en una sola página
├── src/
│   ├── utils/
│   │   ├── seguridad.py        # Cifrado Fernet y hashing SHA-256
│   │   └── excel_exporter.py   # Generación de reportes Excel con openpyxl
│   └── database/
│       ├── conexion.py         # Conexión a SQLite
│       └── tablas.py           # Esquemas de base de datos (5 tablas)
├── tests/                      # Tests de rutas, seguridad y Excel
├── .github/workflows/          # CI/CD y keep-awake del demo
├── locustfile.py               # Simulación de carga
├── pyproject.toml              # Configuración de ruff y pyright
├── Procfile                    # Configuración para Render / Heroku
└── requirements*.txt
```

---

## Puesta en marcha

### Requisitos

- Python 3.11 o superior.

### Local

```bash
git clone https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version.git
cd Online-Inventory-Control-System-Free-Version
pip install -r requirements.txt
python app.py
```

Abre tu navegador en `http://localhost:5000`.

### Producción

```bash
# En Linux
gunicorn app:app

# En Windows
waitress-serve --port=5000 app:app
```

La app ya incluye las cabeceras de seguridad necesarias para producción (CSP, HSTS, X-Frame-Options, etc.).

---

## Detalles del proyecto

- **Cabeceras de seguridad listas para producción**: CSP, HSTS, X-Frame-Options, Permissions-Policy.
- **Cifrado Fernet (AES) y hashing SHA-256** ya implementados, listos si algún día se necesita persistencia del lado del servidor.
- **Reporte Excel con formato profesional**: no es un CSV disfrazado; tiene encabezados azules, anchos de columna ajustados y fórmulas de suma automáticas.
- **CI/CD completo**: linting (ruff), type checking (pyright) y tests en GitHub Actions.
- **Soporte multiplataforma**: Gunicorn en Linux, Waitress en Windows y Procfile listo para Render o Heroku.

### Pruebas de carga con Locust

```bash
pip install locust
locust -f locustfile.py --headless -u 50 -r 5 -H http://localhost:5000
```

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --tb=short
```

Cubren cifrado, generación de Excel y validación de rutas (32 tests en total).

---

## Licencia

Uso educativo y demostrativo. Si encuentras un bug o se te ocurre algo, abre un issue o un PR. Toda contribución es bienvenida.

---

¿Lo prefieres en inglés? → [README.en.md](README.en.md)