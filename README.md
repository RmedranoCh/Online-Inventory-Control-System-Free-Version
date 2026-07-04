# Sistema de Control de Inventario Online — Versión Gratuita

[![CI](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml/badge.svg)](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey)](https://flask.palletsprojects.com)

**Una aplicación web moderna y funcional para gestionar inventarios, registrar ventas y generar reportes contables en Excel.** Construida con Flask en el backend y HTML, CSS y JavaScript puro en el frontend, sin frameworks ni librerías externas del lado del cliente.

Vivo y funcionando en: [https://inventory-control-system-free.onrender.com](https://inventory-control-system-free.onrender.com)

---

## ¿Qué hace esta app?

Digamos que tienes un negocio pequeño, vendes productos y necesitas llevar el control de tu inventario sin complicarte la vida con hojas de cálculo enormes o software caro. Abres esta página, y en segundos puedes:

- **Agregar productos** con nombre, cantidad, costo unitario, stock mínimo y detalles.
- **Editar o eliminar** productos que ya no vendes o que actualizaste.
- **Registrar ventas** y el sistema descuenta automáticamente del stock.
- **Ver un historial completo** de todo lo que ha pasado (altas, bajas, ventas, modificaciones).
- **Exportar un reporte contable profesional en Excel** con dos hojas: el libro contable (Kárdex) y el inventario disponible, con fórmulas incluidas.
- **Sin registro, sin cuentas, sin correos.** Todo se guarda en el navegador (`localStorage`). Tus datos se quedan contigo.

Es una versión gratuita con límites pensados para demostración: máximo 20 productos y hasta 2 exportaciones de Excel por navegador.

---

## ¿Para quién es esto?

- **Reclutadores y entrevistadores técnicos** que quieran ver un proyecto full-stack bien trabajado, con buenas prácticas de seguridad, testing y despliegue.
- **Pequeños negocios** que necesitan un control de inventario rápido y sin instalaciones.
- **Estudiantes y desarrolladores** que quieran aprender o inspirarse viendo cómo está armado.

---

## Lo que me gusta de este proyecto (y lo que lo hace especial)

La idea era construir algo que se sintiera **profesional pero sencillo**. Sin exagerar: seguridad de verdad (no solo decorativa), un Excel que no da pena enviarle a un contador, y un diseño que no lastime los ojos a las 11 de la noche.

Algunas cosas que quizá no se ven a simple vista:

- **Privacidad ante todo.** Tus productos, tus ventas, tu historial. Nunca llegan a un servidor. Solo viven en tu navegador.
- **Cabeceras de seguridad listas para producción.** CSP, HSTS, X-Frame-Options, Permissions-Policy... todo lo que un auditor de seguridad esperaría ver.
- **Cifrado Fernet (AES) y hashing SHA-256** listos para usar si algún día este proyecto necesitara persistencia del lado del servidor.
- **Reporte Excel con nombre y apellido.** No es un CSV disfrazado. Tiene formato profesional, encabezados azules, anchos de columna ajustados, y fórmulas de suma automáticas.
- **Límites validados en dos capas:** en el frontend y en el backend. Porque un buen sistema de demo se cuida de los curiosos.
- **Pruebas automatizadas** que cubren cifrado, generación de Excel y validación de rutas (16 tests en total).
- **CI/CD completo** con linting (ruff), type checking (pyright) y tests en GitHub Actions.
- **Soporte multiplataforma** para producción: Gunicorn en Linux, Waitress en Windows, y Procfile listo para Render o Heroku.

---

## Stack Tecnológico

| Capa          | Tecnología                          |
|---------------|-------------------------------------|
| Backend       | Python 3 + Flask                    |
| Frontend      | HTML5, CSS3, JavaScript (vanilla)   |
| Exportación   | openpyxl (Excel .xlsx)              |
| Seguridad     | cryptography (Fernet AES), SHA-256  |
| Despliegue    | Gunicorn (Linux) / Waitress (Win)   |
| CI/CD         | GitHub Actions (ruff + pyright)     |
| Tests         | pytest (16 tests)                   |
| Carga         | Locust                              |

---

## Cómo usarlo localmente

```bash
git clone https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version.git
cd Online-Inventory-Control-System-Free-Version
pip install -r requirements.txt
python app.py
```

Abre tu navegador en `http://localhost:5000` y ya estás dentro.

### Para desarrollo

Si quieres correr los tests o contribuir:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --tb=short
```

---

## Despliegue en producción

```bash
# En Linux
gunicorn app:app

# En Windows
waitress-serve --port=5000 app:app
```

La app ya incluye todas las cabeceras de seguridad necesarias para producción (CSP, HSTS, X-Frame-Options, etc.).

---

## Pruebas de carga con Locust

```bash
pip install locust
locust -f locustfile.py --headless -u 50 -r 5 -H http://localhost:5000
```

---

## Cómo está organizado el proyecto

```
inventory-control-system/
├── app.py                      # El servidor Flask con la API REST (2 rutas)
├── server.py                   # Punto de entrada multiplataforma
├── run.py                      # Punto de entrada alternativo
├── templates/
│   └── index.html              # La aplicación completa en una sola página
├── tests/
│   ├── test_app.py             # 8 tests de integración de rutas y API
│   ├── test_seguridad.py       # 9 tests unitarios de cifrado y hashing
│   └── test_excel.py           # 5 tests unitarios de exportación Excel
├── src/
│   ├── utils/
│   │   ├── seguridad.py        # Cifrado Fernet y hashing SHA-256
│   │   └── excel_exporter.py   # Generación de reportes Excel con openpyxl
│   └── database/
│       ├── conexion.py         # Conexión a SQLite
│       └── tablas.py           # Esquemas de base de datos (5 tablas)
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD: lint, typecheck, test
│       └── keep-awake.yml      # Ping al demo en Render para evitar cold starts
├── locustfile.py               # Simulación de carga para pruebas
├── pyproject.toml              # Configuración de ruff y pyright
├── requirements.txt            # Dependencias para producción
├── requirements-dev.txt        # Dependencias para desarrollo
├── Procfile                    # Configuración para Render / Heroku
└── README.md
```

---

## Licencia

Uso educativo y demostrativo. Si te sirve, úsalo, estúdialo, mejóralo. Eso sí, si encuentras un bug o se te ocurre algo cool, abre un issue o un PR. Toda contribución es bienvenida.

---

---

# Inventory Control System — Free Version

[![CI](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml/badge.svg)](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey)](https://flask.palletsprojects.com)

**A modern, functional web application for managing inventory, recording sales, and generating accounting reports in Excel.** Built with Flask on the backend and vanilla HTML, CSS, and JavaScript on the frontend — no client-side frameworks or external libraries.

Live demo: [https://inventory-control-system-free.onrender.com](https://inventory-control-system-free.onrender.com)

---

## What It Does

Imagine you run a small business. You sell products and need to keep track of your inventory without drowning in spreadsheets or expensive software. Open this page, and within seconds you can:

- **Add products** with name, quantity, unit cost, minimum stock, and notes.
- **Edit or delete** products you no longer sell or need to update.
- **Record sales** and the system automatically deducts from stock.
- **View a complete history** of everything that's happened (additions, removals, sales, modifications).
- **Export a professional accounting report in Excel** with two sheets: a ledger (Kardex) and available inventory, complete with formulas.
- **No sign-ups, no accounts, no emails.** Everything stays in your browser (`localStorage`). Your data belongs to you.

This is a free demo version with reasonable limits: up to 20 products and 2 Excel exports per browser.

---

## Who Is This For

- **Recruiters and technical interviewers** looking for a polished full-stack project with solid security practices, testing, and deployment.
- **Small business owners** who need quick inventory management without installations.
- **Students and developers** who want to learn or find inspiration from a real-world codebase.

---

## What Makes This Project Special

The goal was to build something that feels **professional yet simple**. Not cutting corners: real security (not just for show), an Excel report you wouldn't be embarrassed to send to an accountant, and a design that doesn't burn your eyes at 11 PM.

Some things you might not notice at first glance:

- **Privacy first.** Your products, sales, and history never reach a server. They live exclusively in your browser.
- **Production-ready security headers.** CSP, HSTS, X-Frame-Options, Permissions-Policy — everything a security auditor would expect.
- **Fernet (AES) encryption and SHA-256 hashing** ready to go if this project ever needs server-side persistence.
- **A proper Excel report.** Not a disguised CSV. It has professional formatting, blue headers, auto-adjusted column widths, and built-in SUM formulas.
- **Two-layer limit validation** on both frontend and backend. A good demo system keeps the curious in check.
- **Automated tests** covering encryption, Excel generation, and route validation (16 tests total).
- **Full CI/CD pipeline** with linting (ruff), type checking (pyright), and tests on GitHub Actions.
- **Cross-platform production support**: Gunicorn on Linux, Waitress on Windows, and a Procfile ready for Render or Heroku.

---

## Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Backend        | Python 3 + Flask                    |
| Frontend       | HTML5, CSS3, JavaScript (vanilla)   |
| Export         | openpyxl (Excel .xlsx)              |
| Security       | cryptography (Fernet AES), SHA-256  |
| Deployment     | Gunicorn (Linux) / Waitress (Win)   |
| CI/CD          | GitHub Actions (ruff + pyright)     |
| Tests          | pytest (16 tests)                   |
| Load Testing   | Locust                              |

---

## Local Setup

```bash
git clone https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version.git
cd Online-Inventory-Control-System-Free-Version
pip install -r requirements.txt
python app.py
```

Open your browser at `http://localhost:5000` and you're in.

### Development

If you want to run the tests or contribute:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --tb=short
```

---

## Production Deployment

```bash
# On Linux
gunicorn app:app

# On Windows
waitress-serve --port=5000 app:app
```

The app already includes all necessary security headers for production (CSP, HSTS, X-Frame-Options, etc.).

---

## Load Testing with Locust

```bash
pip install locust
locust -f locustfile.py --headless -u 50 -r 5 -H http://localhost:5000
```

---

## Project Structure

```
inventory-control-system/
├── app.py                      # Flask server with REST API (2 routes)
├── server.py                   # Cross-platform entry point
├── run.py                      # Alternative entry point
├── templates/
│   └── index.html              # Single-page application (all-in-one)
├── tests/
│   ├── test_app.py             # 8 integration tests for routes and API
│   ├── test_seguridad.py       # 9 unit tests for encryption and hashing
│   └── test_excel.py           # 5 unit tests for Excel export
├── src/
│   ├── utils/
│   │   ├── seguridad.py        # Fernet encryption and SHA-256 hashing
│   │   └── excel_exporter.py   # Excel report generation with openpyxl
│   └── database/
│       ├── conexion.py         # SQLite connection
│       └── tablas.py           # Database schemas (5 tables)
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI/CD: lint, typecheck, test
│       └── keep-awake.yml      # Ping to Render demo to prevent cold starts
├── locustfile.py               # Load testing simulation
├── pyproject.toml              # Ruff and pyright configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Procfile                    # Render / Heroku configuration
└── README.md
```

---

## License

Educational and demonstrative use. If it helps you, use it, study it, improve it. If you find a bug or have a cool idea, open an issue or a PR. All contributions are welcome.
