import tkinter as tk
from tkinter import ttk
from app.views.components.rate_input_frame import RateInputFrame

class CreditInputsFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Datos del Crédito", padding=10)
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure((1, 3), weight=1)

        ttk.Label(self, text="Monto (P):").grid(row=0, column=0, sticky="w", padx=5)
        self.amount_var = tk.StringVar(value="5000000")
        self.amount_entry = ttk.Entry(self, textvariable=self.amount_var)
        self.amount_entry.grid(row=0, column=1, sticky="we", padx=5)

        ttk.Label(self, text="Cuota Objetivo (R):").grid(row=0, column=2, sticky="w", padx=5)
        self.cuota_var = tk.StringVar(value="0")
        self.cuota_entry = ttk.Entry(self, textvariable=self.cuota_var)
        self.cuota_entry.grid(row=0, column=3, sticky="we", padx=5)

        ttk.Label(self, text="Plazo (años):").grid(row=1, column=0, sticky="w", padx=5)
        self.years_var = tk.StringVar(value="3") 
        ttk.Entry(self, textvariable=self.years_var).grid(row=1, column=1, sticky="we", padx=5)
        
        self.rate_frame = RateInputFrame(self)
        self.rate_frame.grid(row=2, column=0, columnspan=4, sticky="we", pady=10)

    def get_data(self):
        rate_data = self.rate_frame.get_values()
        return {
            "amount": self.amount_var.get(),
            "cuota_input": self.cuota_var.get(),
            "years": self.years_var.get(),
            "rate": rate_data["rate"],
            "tipo_tasa": rate_data["tipo_tasa"],
            "periodo_tasa": rate_data["periodo_tasa"],
            "periodicidad": rate_data["periodicidad"]
        }

    def set_mode(self, mode):
        if mode == "calcular_cuota":
            self.amount_entry.config(state="normal")
            self.cuota_entry.config(state="disabled")
            self.cuota_var.set("0")
        else:
            self.amount_entry.config(state="disabled")
            self.amount_var.set("0")
            self.cuota_entry.config(state="normal")