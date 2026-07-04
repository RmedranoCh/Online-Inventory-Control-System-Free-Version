from src.database.conexion import obtener_conexion
from src.utils.seguridad import encriptar_contrasena

def inicializar_base_de_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_token TEXT NOT NULL,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio_costo REAL NOT NULL DEFAULT 0.0,
            detalles TEXT DEFAULT '',
            stock_minimo INTEGER NOT NULL DEFAULT 5,
            UNIQUE(usuario_token, nombre)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_token TEXT NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad_vendida INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total_venta REAL NOT NULL,
            detalles_venta TEXT DEFAULT '',
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_token TEXT NOT NULL,
            producto_id INTEGER,
            tipo_evento TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS limites_usuario (
            usuario_token TEXT PRIMARY KEY,
            productos_creados INTEGER DEFAULT 0,
            archivos_excel_generados INTEGER DEFAULT 0
        );
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (usuario, contrasena)
        VALUES (?, ?)
    """, ("admin", encriptar_contrasena("admin123")))

    conexion.commit()
    conexion.close()
