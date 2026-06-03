import sys
import os
import customtkinter as ctk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.tablas import inicializar_base_de_datos
from src.views.login_view import LoginView
from src.views.dashboard_view import DashboardView

class VentanaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión de Inventario Pro v1.0")
        
        self.resizable(True, True)
        
        self.geometry("1100x700")
        self.minsize(1100, 700)
        
        self.after(0, lambda: self.state('zoomed'))
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)
        
        inicializar_base_de_datos()
        self.mostrar_login()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        self.limpiar_contenedor()
        self.vista_actual = LoginView(self.contenedor, login_exitoso_callback=self.mostrar_dashboard)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        self.limpiar_contenedor()
        self.vista_actual = DashboardView(self.contenedor)
        self.vista_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()