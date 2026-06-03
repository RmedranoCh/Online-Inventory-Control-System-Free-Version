from src.database.conexion import obtener_conexion
from hashlib import sha256

def inicializar_base_de_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio_costo REAL NOT NULL DEFAULT 0.0,
            detalles TEXT,
            stock_minimo INTEGER NOT NULL DEFAULT 5
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad_vendida INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total_venta REAL NOT NULL,
            detalles_venta TEXT,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER, -- Enlace clave para poder limpiar el Excel al borrar el producto
            tipo_evento TEXT NOT NULL, 
            descripcion TEXT NOT NULL,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
        );
    """)
    
    cursor.execute("DROP TRIGGER IF EXISTS log_nuevo_producto;")
    cursor.execute("DROP TRIGGER IF EXISTS log_actualizacion_producto;")
    cursor.execute("DROP TRIGGER IF EXISTS log_nueva_venta;")
    
    cursor.execute("""
        CREATE TRIGGER log_nuevo_producto
        AFTER INSERT ON productos
        BEGIN
            INSERT INTO historial_movimientos (producto_id, tipo_evento, descripcion)
            VALUES (NEW.id, 'CREACION', 'Ingreso: ' || NEW.nombre || ' | Cantidad: ' || NEW.cantidad || ' uds | Costo Unitario: $' || NEW.precio_costo);
        END;
    """)
    
    cursor.execute("""
        CREATE TRIGGER log_actualizacion_producto
        AFTER UPDATE ON productos
        WHEN OLD.cantidad <> NEW.cantidad OR OLD.precio_costo <> NEW.precio_costo
        BEGIN
            INSERT INTO historial_movimientos (producto_id, tipo_evento, descripcion)
            VALUES (
                NEW.id,
                CASE WHEN NEW.cantidad <= NEW.stock_minimo THEN 'BAJO STOCK' ELSE 'ACTUALIZACION' END,
                'Modificación: ' || NEW.nombre || ' | Cambio Stock: ' || OLD.cantidad || '->' || NEW.cantidad || ' | Costo Unitario: $' || NEW.precio_costo
            );
        END;
    """)

    cursor.execute("""
        CREATE TRIGGER log_nueva_venta
        AFTER INSERT ON ventas
        BEGIN
            INSERT INTO historial_movimientos (producto_id, tipo_evento, descripcion)
            VALUES (NEW.producto_id, 'VENTA', 'Salida de stock | Cantidad: ' || NEW.cantidad_vendida || ' uds | Precio Venta: $' || NEW.precio_unitario);
        END;
    """)

    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin';")
    if not cursor.fetchone():
        contrasena_segura = sha256("admin123".encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?);", ("admin", contrasena_segura))
        
    conexion.commit()
    conexion.close()