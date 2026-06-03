import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from src.database.conexion import obtener_conexion
from src.utils.seguridad import desencriptar_dato

def generar_reporte_completo_excel(ruta_guardado: str) -> bool:
    try:
        libro = openpyxl.Workbook()
        
        fuente_cabecera = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        fuente_total = Font(name="Calibri", size=11, bold=True, color="000000")
        relleno_cabecera = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        relleno_total = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
        alineacion_centro = Alignment(horizontal="center", vertical="center")
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        ws_kardex = libro.active
        ws_kardex.title = "Libro Contable"
        ws_kardex.append([
            "Fecha y Hora", 
            "Detalle / Operación", 
            "Cantidad Movida", 
            "Precio Unitario ($)", 
            "Entradas (Costo Total) ($)", 
            "Salidas (Venta Total) ($)", 
            "Saldo Neto ($)"
        ])
        
        cursor.execute("""
            SELECT hm.fecha_hora, hm.tipo_evento, hm.descripcion 
            FROM historial_movimientos hm
            LEFT JOIN productos p ON hm.producto_id = p.id
            WHERE hm.tipo_evento != 'ELIMINACION' 
              AND (hm.producto_id IS NULL OR p.id IS NOT NULL)
            ORDER BY hm.id ASC
        """)
        
        fila_actual = 2
        for fecha, tipo, desc in cursor.fetchall():
            cantidad_piezas = 0
            precio_unitario = 0.0
            entrada_total = 0.0
            salida_total = 0.0
            
            try:
                if tipo in ["CREACION", "ACTUALIZACION"] and "cantidad:" in desc.lower():
                    partes = desc.split("|")
                    for parte in partes:
                        if "cantidad:" in parte.lower():
                            cantidad_piezas = int(parte.split(":")[-1].replace("uds", "").strip())
                        if "costo unitario:" in parte.lower():
                            precio_unitario = float(parte.split("$")[-1].strip())
                    entrada_total = cantidad_piezas * precio_unitario
                
                elif tipo == "VENTA":
                    partes = desc.split("|")
                    for parte in partes:
                        if "cantidad:" in parte.lower():
                            cantidad_piezas = int(parte.split(":")[-1].replace("uds", "").strip())
                        if "precio venta:" in parte.lower():
                            precio_unitario = float(parte.split("$")[-1].strip())
                    salida_total = cantidad_piezas * precio_unitario
            except:
                pass 
                
            saldo_neto = salida_total - entrada_total
            ws_kardex.append([fecha, desc, cantidad_piezas, precio_unitario, entrada_total, salida_total, saldo_neto])
            fila_actual += 1
            
        ws_kardex.append([
            "TOTALES", 
            "Sumatoria global analítica", 
            "-", 
            "-", 
            f"=SUM(E2:E{fila_actual-1})", 
            f"=SUM(F2:F{fila_actual-1})", 
            f"=SUM(G2:G{fila_actual-1})"
        ])
        
        for col_idx in range(1, 8):
            celda_tot = ws_kardex.cell(row=fila_actual, column=col_idx)
            celda_tot.font = fuente_total
            celda_tot.fill = relleno_total

        ws_inventario = libro.create_sheet(title="Inventario Disponible")
        ws_inventario.append(["ID Producto", "Nombre", "Cantidad en Stock", "Costo Adquisición Unitario ($)", "Detalles", "Stock Mínimo"])
        
        cursor.execute("SELECT id, nombre, cantidad, precio_costo, detalles, stock_minimo FROM productos")
        for fila in cursor.fetchall():
            lista_fila = list(fila)
            detalles_encriptados = lista_fila[4]
            lista_fila[4] = desencriptar_dato(detalles_encriptados)
            ws_inventario.append(lista_fila)
            
        conexion.close()
        
        for hoja in libro.worksheets:
            for col_idx in range(1, hoja.max_column + 1):
                celda = hoja.cell(row=1, column=col_idx)
                celda.font = fuente_cabecera
                celda.fill = relleno_cabecera
                celda.alignment = alineacion_centro
            
            for col in hoja.columns:
                max_len = 0
                col_letter = get_column_letter(col[0].column)
                for cell in col:
                    if cell.value is not None:
                        max_len = max(max_len, len(str(cell.value)))
                hoja.column_dimensions[col_letter].width = max(max_len + 4, 16)
                
        libro.save(ruta_guardado)
        return True
        
    except Exception as e:
        print(f"Error en el libro contable Excel: {e}")
        return False