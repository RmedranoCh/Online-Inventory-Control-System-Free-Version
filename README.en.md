# Inventory Control System — Free Version

[![CI](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml/badge.svg)](https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-lightgrey)](https://flask.palletsprojects.com)

A modern web app for managing inventory, recording sales, and generating accounting reports in Excel. Built with **Flask** on the backend and **vanilla HTML, CSS, and JavaScript** on the frontend — no client-side frameworks or external libraries.

Live demo: https://inventory-control-system-free.onrender.com

---

## Features

- **No sign-ups, no accounts, no emails**: everything is stored in the browser (`localStorage`). Your data stays with you and never reaches a server.
- **Product management**: add products with name, quantity, unit cost, minimum stock, and notes; edit or delete them whenever you want.
- **Sales registration** with automatic stock deduction.
- **Complete history** of everything that has happened (additions, removals, sales, modifications).
- **Accounting report in Excel** with two sheets: a ledger (Kardex) and available inventory, including formulas.
- **Limits validated on two layers** (frontend and backend): up to 20 products and 2 Excel exports per browser. Designed for demonstration.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3 + Flask |
| **Frontend** | HTML5, CSS3, vanilla JavaScript |
| **Export** | openpyxl (Excel .xlsx) |
| **Security** | cryptography (Fernet AES), SHA-256 |
| **Deployment** | Gunicorn (Linux) / Waitress (Windows) |
| **CI/CD** | GitHub Actions (ruff + pyright) |
| **Tests** | pytest (32 tests) |
| **Load testing** | Locust |

---

## Project structure

```
inventory-control-system/
├── app.py                      # Flask server with the REST API
├── server.py                   # Cross-platform entry point
├── run.py                      # Alternative entry point
├── templates/
│   └── index.html              # The complete app in a single page
├── src/
│   ├── utils/
│   │   ├── seguridad.py        # Fernet encryption and SHA-256 hashing
│   │   └── excel_exporter.py   # Excel report generation with openpyxl
│   └── database/
│       ├── conexion.py         # SQLite connection
│       └── tablas.py           # Database schemas (5 tables)
├── tests/                      # Route, security, and Excel tests
├── .github/workflows/          # CI/CD and keep-awake for the demo
├── locustfile.py               # Load testing simulation
├── pyproject.toml              # Ruff and pyright configuration
├── Procfile                    # Render / Heroku configuration
└── requirements*.txt
```

---

## Getting started

### Requirements

- Python 3.11 or later.

### Locally

```bash
git clone https://github.com/RmedranoCh/Online-Inventory-Control-System-Free-Version.git
cd Online-Inventory-Control-System-Free-Version
pip install -r requirements.txt
python app.py
```

Open your browser at `http://localhost:5000`.

### Production

```bash
# On Linux
gunicorn app:app

# On Windows
waitress-serve --port=5000 app:app
```

The app already includes the security headers required for production (CSP, HSTS, X-Frame-Options, etc.).

---

## Project details

- **Production-ready security headers**: CSP, HSTS, X-Frame-Options, Permissions-Policy.
- **Fernet (AES) encryption and SHA-256 hashing** already in place, ready if the project ever needs server-side persistence.
- **A proper Excel report**: not a disguised CSV; it has blue headers, adjusted column widths, and automatic SUM formulas.
- **Full CI/CD**: linting (ruff), type checking (pyright), and tests on GitHub Actions.
- **Cross-platform support**: Gunicorn on Linux, Waitress on Windows, and a Procfile ready for Render or Heroku.

### Load testing with Locust

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

They cover encryption, Excel generation, and route validation (32 tests total).

---

## License

Educational and demonstrative use. If you find a bug or have an idea, open an issue or a PR. All contributions are welcome.

---

Prefer Spanish? → [README.md](README.md)