import customtkinter as ctk
from tkinter import messagebox
from src.database.conexion import obtener_conexion
from src.utils.seguridad import verificar_contrasena

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, login_exitoso_callback):
        super().__init__(parent, fg_color=("#F2F4F7", "#0F172A"))
        self.login_exitoso_callback = login_exitoso_callback
        
        self.card = ctk.CTkFrame(self, width=420, height=480, corner_radius=24, fg_color=("#FFFFFF", "#1E293B"))
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.card, text="SISTEMA CONTROL PRO", font=("Segoe UI", 26, "bold"), text_color=("#1E40AF", "#3B82F6")
        )
        self.title_label.pack(pady=(45, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.card, text="Gestión Avanzada de Activos & Kárdex", font=("Segoe UI", 13), text_color=("#64748B", "#94A3B8")
        )
        self.subtitle_label.pack(pady=(0, 35))
        
        self.user_entry = ctk.CTkEntry(
            self.card, placeholder_text="Nombre de Usuario", width=320, height=48, corner_radius=12,
            font=("Segoe UI", 14), fg_color=("#F8FAFC", "#0F172A"), border_color=("#CBD5E1", "#334155")
        )
        self.user_entry.pack(pady=12)
        
        self.pass_entry = ctk.CTkEntry(
            self.card, placeholder_text="Contraseña Oculta", show="*", width=320, height=48, corner_radius=12,
            font=("Segoe UI", 14), fg_color=("#F8FAFC", "#0F172A"), border_color=("#CBD5E1", "#334155")
        )
        self.pass_entry.pack(pady=12)
        
        self.login_btn = ctk.CTkButton(
            self.card, text="Iniciar Sesión Seguro", font=("Segoe UI", 14, "bold"),
            width=320, height=48, corner_radius=12, fg_color=("#2563EB", "#3B82F6"),
            hover_color=("#1D4ED8", "#2563EB"), command=self.autenticar
        )
        self.login_btn.pack(pady=40)

    def autenticar(self):
        usuario = self.user_entry.get().strip()
        contrasena = self.pass_entry.get().strip()
        
        if not usuario or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos de acceso.")
            return
            
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado and verificar_contrasena(contrasena, resultado[0]):
            self.login_exitoso_callback()
        else:
            messagebox.showerror("Acceso Denegado", "El usuario o la contraseña ingresada no son correctos.")