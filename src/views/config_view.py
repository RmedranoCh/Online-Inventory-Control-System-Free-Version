import customtkinter as ctk
from tkinter import messagebox
from src.database.conexion import obtener_conexion
from src.utils.seguridad import encriptar_contrasena

class ConfigView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        card = ctk.CTkFrame(self, width=450, height=480, corner_radius=15)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text="Actualizar Credenciales de Acceso", font=("Arial", 18, "bold"), text_color="#1f77b4").pack(pady=20)
        
        self.ent_pass_actual = ctk.CTkEntry(card, placeholder_text="Contraseña Actual Obligatoria", show="*", width=320, height=40)
        self.ent_pass_actual.pack(pady=10)
        
        ctk.CTkLabel(card, text="Nuevos Datos", font=("Arial", 12, "italic"), text_color="gray").pack(pady=5)
        
        self.ent_nuevo_usuario = ctk.CTkEntry(card, placeholder_text="Nuevo Nombre de Usuario", width=320, height=40)
        self.ent_nuevo_usuario.pack(pady=10)
        
        self.ent_nueva_pass = ctk.CTkEntry(card, placeholder_text="Nueva Contraseña Segura", show="*", width=320, height=40)
        self.ent_nueva_pass.pack(pady=10)
        
        btn_actualizar = ctk.CTkButton(card, text="Guardar Cambios de Seguridad", fg_color="green", height=40, command=self.actualizar_seguridad)
        btn_actualizar.pack(pady=30)

    def actualizar_seguridad(self):
        actual = self.ent_pass_actual.get().strip()
        nuevo_user = self.ent_nuevo_usuario.get().strip()
        nueva_p = self.ent_nueva_pass.get().strip()
        
        if not actual or not nuevo_user or not nueva_p:
            messagebox.showwarning("Atención", "Todos los campos son requeridos por auditoría de seguridad.")
            return
            
        hash_actual = encriptar_contrasena(actual)
        hash_nuevo = encriptar_contrasena(nueva_p)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id FROM usuarios WHERE contrasena = ?", (hash_actual,))
        usuario_valido = cursor.fetchone()
        
        if not usuario_valido:
            messagebox.showerror("Error de Validación", "La contraseña actual es incorrecta. No se pueden aplicar cambios.")
            conexion.close()
            return
            
        try:
            cursor.execute("UPDATE usuarios SET usuario = ?, contrasena = ? WHERE id = ?", (nuevo_user, hash_nuevo, usuario_valido[0]))
            conexion.commit()
            messagebox.showinfo("Éxito", "Credenciales del sistema actualizadas correctamente.")
            
            self.ent_pass_actual.delete(0, 'end')
            self.ent_nuevo_usuario.delete(0, 'end')
            self.ent_nueva_pass.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"El nombre de usuario ya está en uso: {e}")
        finally:
            conexion.close()