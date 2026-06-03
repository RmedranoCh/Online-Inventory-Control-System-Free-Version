import customtkinter as ctk
from src.views.inventario_view import InventarioView
from src.views.ventas_view import VentasView
from src.views.config_view import ConfigView

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=("#F8FAFC", "#0F172A"))
        
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=("#FFFFFF", "#1E293B"), border_color=("#E2E8F0", "#334155"), border_width=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.brand_lbl = ctk.CTkLabel(self.sidebar, text="DASHBOARD", font=("Segoe UI", 18, "bold"), text_color=("#1E40AF", "#3B82F6"))
        self.brand_lbl.pack(pady=45)
        
        self.btn_inv = ctk.CTkButton(
            self.sidebar, text="📦  Inventario Real", font=("Segoe UI", 14, "bold"), height=50, corner_radius=12, command=self.cargar_inventario
        )
        self.btn_inv.pack(pady=8, padx=20, fill="x")
        
        self.btn_ventas = ctk.CTkButton(
            self.sidebar, text="🛒  Registrar Ventas", font=("Segoe UI", 14, "bold"), height=50, corner_radius=12, command=self.cargar_ventas
        )
        self.btn_ventas.pack(pady=8, padx=20, fill="x")
        
        self.btn_config = ctk.CTkButton(
            self.sidebar, text="⚙️  Seguridad / Claves", font=("Segoe UI", 14, "bold"), height=50, corner_radius=12, command=self.cargar_config)
        self.btn_config.pack(pady=8, padx=20, fill="x")
        
        self.logout_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logout_frame.pack(side="bottom", fill="x", pady=30, padx=20)
        
        btn_logout = ctk.CTkButton(
            self.logout_frame, text="🔒 Cerrar Sesión", font=("Segoe UI", 13, "bold"), fg_color=("#EF4444", "#DC2626"), hover_color=("#DC2626", "#B91C1C"), height=40, corner_radius=10,
            command=lambda: parent.master.mostrar_login()
        )
        btn_logout.pack(fill="x")
        
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=25, pady=25)
        
        self.vista_actual = None
        self.cargar_inventario()

    def reset_botones(self):
        for btn in [self.btn_inv, self.btn_ventas, self.btn_config]:
            btn.configure(fg_color="transparent", text_color=("#334155", "#94A3B8"), hover_color=("#F1F5F9", "#334155"))

    def cargar_inventario(self):
        self.reset_botones()
        self.btn_inv.configure(fg_color=("#2563EB", "#3B82F6"), text_color="white", hover_color=("#1D4ED8", "#2563EB"))
        if self.vista_actual: self.vista_actual.destroy()
        self.vista_actual = InventarioView(self.main_content)
        self.vista_actual.pack(fill="both", expand=True)

    def cargar_ventas(self):
        self.reset_botones()
        self.btn_ventas.configure(fg_color=("#2563EB", "#3B82F6"), text_color="white", hover_color=("#1D4ED8", "#2563EB"))
        if self.vista_actual: self.vista_actual.destroy()
        self.vista_actual = VentasView(self.main_content)
        self.vista_actual.pack(fill="both", expand=True)

    def cargar_config(self):
        self.reset_botones()
        self.btn_config.configure(fg_color=("#2563EB", "#3B82F6"), text_color="white", hover_color=("#1D4ED8", "#2563EB"))
        if self.vista_actual: self.vista_actual.destroy()
        self.vista_actual = ConfigView(self.main_content)
        self.vista_actual.pack(fill="both", expand=True)