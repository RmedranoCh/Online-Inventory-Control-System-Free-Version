# 📦 Sistema Profesional de Gestión de Inventario & Kárdex Contable

Un software de escritorio de alta gama, moderno e intuitivo, desarrollado en **Python** con **CustomTkinter** y **SQLite**. Diseñado para operar de manera local en una sola computadora de forma rápida, eficiente y completamente segura.

## ✨ Características Principales

*   **🔒 Seguridad Avanzada**: Módulo impenetrable de control de acceso. Las contraseñas se protegen mediante hashes criptográficos **SHA-256** de carácter irreversible.
*   **👁️ Cifrado Oculto de Datos**: Los archivos de base de datos se almacenan de forma invisible en el directorio del sistema operativo (`%AppData%`). Campos sensibles como los comentarios están cifrados localmente mediante el algoritmo **Fernet (AES de 128 bytes)**.
*   **📈 Kárdex Contable Automatizado**: Monitoreo analítico de stock en tiempo real. Diferenciación estricta entre **Costo de Adquisición Unitario** (Entradas de inversión) y **Precio Pactado** (Salidas de ganancias).
*   **🚨 Alertas Visuales Dinámicas**: El sistema resalta de manera automática e inmediata en color rojo los productos cuyo stock actual sea igual o inferior a su límite mínimo configurado.
*   **📊 Reportes Maestros de un Solo Clic**: Generación automatizada de un libro contable estilizado en Microsoft Excel corporativo, con autoajuste de columnas y fórmulas de sumatorias de saldos integradas nativamente.
*   **🗑️ Gestión de Errores Operativos**: Botón de eliminación en cascada (`ON DELETE CASCADE`) que limpia la bitácora financiera si inyectaste mal un producto, manteniendo el balance matemático del Excel perfecto.
*   **🖥️ Interfaz Optimizada**: Diseño responsive adaptado a pantalla completa que respeta el modo oscuro/claro nativo del sistema operativo del usuario.

---

## 📂 Estructura del Proyecto

```text
inventory-control-system/
│
├── src/
│   ├── main.py                  # Punto de arranque y control de pantallas
│   ├── database/
│   │   ├── conexion.py          # Enrutamiento oculto en %AppData%
│   │   └── tablas.py            # Esquemas relacionales y Triggers de SQL
│   ├── views/
│   │   ├── login_view.py        # Control de acceso seguro
│   │   ├── dashboard_view.py    # Navegación del menú lateral
│   │   ├── inventario_view.py   # Formulario e inyección de activos
│   │   ├── ventas_view.py       # Menú desplegable dinámico y cobros
│   │   └── config_view.py       # Cambio auditor de credenciales
│   └── utils/
│       ├── seguridad.py         # Motores criptográficos (SHA-256 / Fernet)
│       └── excel_exporter.py    # Compilador y formateador de Libro Contable
│
├── requirements.txt             # Dependencias del sistema
└── README.md                    # Documentación técnica
```

---

## 🚀 Instalación y Despliegue en Desarrollo

1. **Clonar o descargar** este repositorio en tu directorio local de programación.
2. Abrir una terminal de comandos (PowerShell) en la carpeta raíz del proyecto e instalar las dependencias con un comando único:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la aplicación en entorno interactivo:
   ```bash
   python src/main.py
   ```

### 🗝️ Credenciales de Acceso por Defecto
Al iniciar por primera vez, el sistema inyectará la cuenta de administración maestra:
*   **Usuario**: `admin`
*   **Contraseña**: `admin123`
*(Puedes modificarlas de forma segura en cualquier momento desde la pestaña "Seguridad / Claves")*.

---

## 📦 Compilación a Botón de Arranque Directo (`.exe`)

Para compilar todo el proyecto en un único archivo ejecutable independiente que abra directamente con doble clic sin necesidad de instalar librerías adicionales, ejecuta el siguiente comando:

```bash
pyinstaller --clean --noconsole --onefile src/main.py
```

### 🎯 Resultados del Empaquetado:
*   El archivo compilado definitivo llamado `main.exe` aparecerá dentro de la carpeta **`dist/`**.
*   Puedes cambiarle el nombre a `SistemaContable.exe`, moverlo al Escritorio y borrar las carpetas temporales sobrantes (`build/` y `main.spec`).
