import customtkinter as ctk
from tkinter import messagebox, filedialog
from src.database.conexion import obtener_conexion
from src.utils.excel_exporter import generar_reporte_completo_excel
from src.utils.seguridad import encriptar_dato, desencriptar_dato

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.form_frame = ctk.CTkFrame(self, width=340)
        self.form_frame.pack(side="left", fill="y", padx=(0, 15))
        self.form_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.form_frame, text="Operación de Producto", font=("Arial", 22, "bold"), text_color="#1f77b4").pack(pady=25)
        
        self.ent_nombre = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre único del producto", width=280, height=45, font=("Arial", 14))
        self.ent_nombre.pack(pady=10)
        
        self.ent_cantidad = ctk.CTkEntry(self.form_frame, placeholder_text="Cantidad en Stock", width=280, height=45, font=("Arial", 14))
        self.ent_cantidad.pack(pady=10)
        
        self.ent_precio = ctk.CTkEntry(self.form_frame, placeholder_text="Costo Unitario Producto ($)", width=280, height=45, font=("Arial", 14))
        self.ent_precio.pack(pady=10)
        
        self.ent_minimo = ctk.CTkEntry(self.form_frame, placeholder_text="Stock Mínimo Alerta (Ej: 5)", width=280, height=45, font=("Arial", 14))
        self.ent_minimo.pack(pady=10)
        
        self.ent_detalles = ctk.CTkEntry(self.form_frame, placeholder_text="Detalles adicionales", width=280, height=45, font=("Arial", 14))
        self.ent_detalles.pack(pady=10)
        
        btn_guardar = ctk.CTkButton(self.form_frame, text="Inyectar / Actualizar", font=("Arial", 14, "bold"), fg_color="green", hover_color="darkgreen", height=45, command=self.procesar_producto)
        btn_guardar.pack(pady=(20, 10), padx=25, fill="x")
        
        btn_borrar = ctk.CTkButton(self.form_frame, text="🗑️ Eliminar Producto", font=("Arial", 14, "bold"), fg_color="#bb2124", hover_color="#7a1518", height=45, command=self.eliminar_producto)
        btn_borrar.pack(pady=10, padx=25, fill="x")
        
        btn_excel = ctk.CTkButton(self.form_frame, text="📊 Generar Libro Contable", font=("Arial", 14, "bold"), fg_color="#1f77b4", height=45, command=self.exportar_datos)
        btn_excel.pack(pady=10, padx=25, fill="x")
        
        self.table_container = ctk.CTkScrollableFrame(self, label_text="Monitoreo de Inventario en Tiempo Real")
        self.table_container.pack(side="right", fill="both", expand=True)
        
        self.renderizar_tabla()

    def renderizar_tabla(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()
            
        cabeceras = ["Nombre Producto", "Stock Actual", "Costo Unitario ($)", "Mínimo Alerta", "Detalles"]
        for col_idx, texto in enumerate(cabeceras):
            lbl = ctk.CTkLabel(self.table_container, text=texto, font=("Arial", 14, "bold"), text_color="#1f77b4")
            lbl.grid(row=0, column=col_idx, padx=15, pady=12, sticky="w")
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, cantidad, precio_costo, stock_minimo, detalles FROM productos")
        
        for row_idx, fila in enumerate(cursor.fetchall(), start=1):
            nombre, cantidad, precio, min_alerta, detalles_encriptados = fila
            detalles = desencriptar_dato(detalles_encriptados)
            
            es_alerta = cantidad <= min_alerta
            color_texto = "#ff5555" if es_alerta else ("#000000", "#FFFFFF")
            peso_fuente = "bold" if es_alerta else "normal"
            mostrar_nombre = f"⚠️ {nombre}" if es_alerta else nombre
            
            ctk.CTkLabel(self.table_container, text=mostrar_nombre, text_color=color_texto, font=("Arial", 13, peso_fuente)).grid(row=row_idx, column=0, padx=15, pady=8, sticky="w")
            ctk.CTkLabel(self.table_container, text=str(cantidad), text_color=color_texto, font=("Arial", 13, peso_fuente)).grid(row=row_idx, column=1, padx=15, pady=8, sticky="w")
            ctk.CTkLabel(self.table_container, text=f"${precio:.2f}", text_color=color_texto, font=("Arial", 13)).grid(row=row_idx, column=2, padx=15, pady=8, sticky="w")
            ctk.CTkLabel(self.table_container, text=str(min_alerta), text_color="gray", font=("Arial", 13)).grid(row=row_idx, column=3, padx=15, pady=8, sticky="w")
            ctk.CTkLabel(self.table_container, text=str(detalles), text_color="gray", font=("Arial", 13)).grid(row=row_idx, column=4, padx=15, pady=8, sticky="w")
            
        conexion.close()

    def procesar_producto(self):
        nombre = self.ent_nombre.get().strip()
        cantidad_txt = self.ent_cantidad.get().strip()
        precio_txt = self.ent_precio.get().strip()
        minimo_txt = self.ent_minimo.get().strip() or "5"
        detalles = self.ent_detalles.get().strip()
        
        if not (nombre and cantidad_txt and precio_txt):
            messagebox.showwarning("Atención", "Nombre, Cantidad y Costo son obligatorios.")
            return
            
        try:
            cantidad = int(cantidad_txt)
            precio = float(precio_txt)
            minimo = int(minimo_txt)
            if cantidad < 0 or precio < 0 or minimo < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Formatos numéricos inválidos.")
            return

        detalles_seguros = encriptar_dato(detalles)
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.execute("UPDATE productos SET cantidad=?, precio_costo=?, stock_minimo=?, detalles=? WHERE nombre=?", (cantidad, precio, minimo, detalles_seguros, nombre))
        else:
            cursor.execute("INSERT INTO productos (nombre, cantidad, precio_costo, stock_minimo, detalles) VALUES (?, ?, ?, ?, ?)", (nombre, cantidad, precio, minimo, detalles_seguros))
            
        conexion.commit()
        conexion.close()
        
        self.renderizar_tabla()
        self.limpiar_campos()

    def eliminar_producto(self):
        nombre = self.ent_nombre.get().strip()
        
        if not nombre:
            messagebox.showwarning("Falta Información", "Por favor escribe el nombre exacto del producto que deseas eliminar en el primer campo del formulario.")
            return
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        producto = cursor.fetchone()
        
        if not producto:
            messagebox.showerror("No Encontrado", f"No se encontró ningún producto con el nombre '{nombre}' para eliminar.")
            conexion.close()
            return
            
        confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Estás completamente seguro de eliminar '{nombre}' del inventario?\nEsta acción no se puede deshacer.")
        if confirmacion:
            cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
            
            cursor.execute("INSERT INTO historial_movimientos (tipo_evento, descripcion) VALUES ('ELIMINACION', 'Se eliminó del inventario el producto: ' || ?)", (nombre,))
            
            conexion.commit()
            messagebox.showinfo("Éxito", f"Producto '{nombre}' eliminado correctamente del sistema.")
            
        conexion.close()
        self.renderizar_tabla()
        self.limpiar_campos()

    def limpiar_campos(self):
        for entrada in [self.ent_nombre, self.ent_cantidad, self.ent_precio, self.ent_minimo, self.ent_detalles]:
            entrada.delete(0, 'end')

    def exportar_datos(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Ledger", "*.xlsx")])
        if ruta:
            if generar_reporte_completo_excel(ruta):
                messagebox.showinfo("Exportación Exitosa", f"Libro Contable Maestro compilado en:\n{ruta}")
            else:
                messagebox.showerror("Fallo", "Error al escribir el reporte.")