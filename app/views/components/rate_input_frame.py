import tkinter as tk
from tkinter import ttk

class RateInputFrame(ttk.LabelFrame):
    def __init__(self, parent, title="Configuración de Tasa"):
        super().__init__(parent, text=title, padding=10)
        self._create_widgets()

    def _create_widgets(self):
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure((1, 3), weight=1)

        ttk.Label(self, text="Tasa (%):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.rate_var = tk.StringVar(value="12")
        ttk.Entry(self, textvariable=self.rate_var).grid(row=0, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(self, text="Tipo de Tasa:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.tipo_tasa_var = tk.StringVar(value="Efectiva")
        ttk.Combobox(self, textvariable=self.tipo_tasa_var, values=("Nominal", "Efectiva"), state="readonly").grid(row=0, column=3, sticky="we", padx=5, pady=2)

        ttk.Label(self, text="Periodo de la Tasa:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.periodo_tasa_var = tk.StringVar(value="Anual")
        ttk.Combobox(self, textvariable=self.periodo_tasa_var, values=("Anual", "Semestral", "Trimestral", "Mensual"), state="readonly").grid(row=1, column=1, sticky="we", padx=5, pady=2)

        ttk.Label(self, text="Frecuencia Pago/Cap.:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.periodicidad_var = tk.StringVar(value="Mensual")
        ttk.Combobox(self, textvariable=self.periodicidad_var, values=("Mensual", "Trimestral", "Semestral", "Anual"), state="readonly").grid(row=1, column=3, sticky="we", padx=5, pady=2)

    def get_values(self):
        return {
            "rate": self.rate_var.get(),
            "tipo_tasa": self.tipo_tasa_var.get(),
            "periodo_tasa": self.periodo_tasa_var.get(),
            "periodicidad": self.periodicidad_var.get()
        }