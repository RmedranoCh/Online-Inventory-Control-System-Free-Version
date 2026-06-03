import customtkinter as ctk
from tkinter import messagebox
from src.database.conexion import obtener_conexion

class VentasView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.box_venta = ctk.CTkFrame(self, height=240)
        self.box_venta.pack(side="top", fill="x", pady=(0, 15))
        self.box_venta.pack_propagate(False)
        
        ctk.CTkLabel(self.box_venta, text="Registrar Salida / Venta Comercial", font=("Arial", 14, "bold"), text_color="#1f77b4").pack(pady=5)
        
        self.form_row = ctk.CTkFrame(self.box_venta, fg_color="transparent")
        self.form_row.pack(pady=10)
        
        ctk.CTkLabel(self.form_row, text="Producto disponible:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.productos_disponibles = self.obtener_lista_productos_con_stock()
        self.dropdown_productos = ctk.CTkOptionMenu(self.form_row, values=self.productos_disponibles, width=220)
        self.dropdown_productos.grid(row=1, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_row, text="Cantidad:", font=("Arial", 11)).grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.ent_cant_vender = ctk.CTkEntry(self.form_row, placeholder_text="Ej: 1", width=90)
        self.ent_cant_vender.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_row, text="Precio Pactado ($):", font=("Arial", 11)).grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.ent_precio_real = ctk.CTkEntry(self.form_row, placeholder_text="Ej: 950.00", width=120)
        self.ent_precio_real.grid(row=1, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(self.form_row, text="Notas / Detalles de esta venta:", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.ent_nota_venta = ctk.CTkEntry(self.form_row, placeholder_text="Ej: Descuento aplicado por pago en efectivo", width=330)
        self.ent_nota_venta.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.btn_ejecutar_venta = ctk.CTkButton(self.form_row, text="⚡ Ejecutar Venta", fg_color="green", hover_color="darkgreen", height=35, command=self.vender)
        self.btn_ejecutar_venta.grid(row=3, column=2, padx=10, pady=5)

        self.historial_container = ctk.CTkScrollableFrame(self, label_text="Bitácora de Operaciones")
        self.historial_container.pack(side="bottom", fill="both", expand=True)
        
        self.renderizar_historial()

    def obtener_lista_productos_con_stock(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos WHERE cantidad > 0")
        items = [row[0] for row in cursor.fetchall()]
        conexion.close()
        return items if items else ["No hay productos con stock"]

    def refrescar_desplegable(self):
        nuevos_valores = self.obtener_lista_productos_con_stock()
        self.dropdown_productos.configure(values=nuevos_valores)
        self.dropdown_productos.set(nuevos_valores[0])

    def renderizar_historial(self):
        for widget in self.historial_container.winfo_children():
            widget.destroy()
            
        cabeceras = ["Registro Temporal", "Categoría Evento", "Descripción de Acción"]
        for col_idx, txt in enumerate(cabeceras):
            ctk.CTkLabel(self.historial_container, text=txt, font=("Arial", 11, "bold"), text_color="#1f77b4").grid(row=0, column=col_idx, padx=15, pady=5, sticky="w")
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT fecha_hora, tipo_evento, descripcion FROM historial_movimientos ORDER BY id DESC")
        
        for row_idx, fila in enumerate(cursor.fetchall(), start=1):
            fecha, tipo, desc = fila
            color_evento = "orange" if tipo == "ACTUALIZACION" else ("green" if tipo == "VENTA" else ("#ff5555" if tipo == "BAJO STOCK" else ("#000000", "#FFFFFF")))
            
            ctk.CTkLabel(self.historial_container, text=str(fecha), text_color="gray").grid(row=row_idx, column=0, padx=15, pady=3, sticky="w")
            ctk.CTkLabel(self.historial_container, text=str(tipo), text_color=color_evento, font=("Arial", 11, "bold")).grid(row=row_idx, column=1, padx=15, pady=3, sticky="w")
            ctk.CTkLabel(self.historial_container, text=str(desc)).grid(row=row_idx, column=2, padx=15, pady=3, sticky="w")
            
        conexion.close()

    def vender(self):
        nombre_prod = self.dropdown_productos.get()
        cantidad_txt = self.ent_cant_vender.get().strip()
        precio_txt = self.ent_precio_real.get().strip()
        nota_venta = self.ent_nota_venta.get().strip() or "Venta estándar directa"
        
        if nombre_prod == "No hay productos con stock" or not cantidad_txt or not precio_txt:
            messagebox.showwarning("Atención", "Por favor selecciona un producto e introduce la cantidad y el precio pactado.")
            return
            
        try:
            cant_vender = int(cantidad_txt)
            precio_real = float(precio_txt)
            if cant_vender <= 0 or precio_real < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser entero positivo y el precio un número válido.")
            return
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, cantidad FROM productos WHERE nombre = ?", (nombre_prod,))
        producto = cursor.fetchone()
        
        if not producto:
            messagebox.showerror("Error", "El producto ya no está disponible.")
            conexion.close()
            return
            
        p_id, stock_actual = producto
        
        if stock_actual < cant_vender:
            messagebox.showerror("Stock Insuficiente", f"Solo quedan {stock_actual} unidades de {nombre_prod}.")
            conexion.close()
            return
            
        nuevo_stock = stock_actual - cant_vender
        total_vta = cant_vender * precio_real
        
        cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nuevo_stock, p_id))
        cursor.execute("INSERT INTO ventas (producto_id, cantidad_vendida, precio_unitario, total_venta, detalles_venta) VALUES (?, ?, ?, ?, ?)", (p_id, cant_vender, precio_real, total_vta, nota_venta))
        
        conexion.commit()
        conexion.close()
        
        messagebox.showinfo("Venta Exitosa", f"Transacción guardada.\nTotal: ${total_vta:.2f}")
        
        self.ent_cant_vender.delete(0, 'end')
        self.ent_precio_real.delete(0, 'end')
        self.ent_nota_venta.delete(0, 'end')
        
        self.refrescar_desplegable()
        self.renderizar_historial()