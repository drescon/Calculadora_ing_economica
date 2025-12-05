import tkinter as tk
from tkinter import ttk, messagebox
from app.views.components.rate_input_frame import RateInputFrame
from app.utils.validators import validate_number

class AnnuityFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Simulador de Anualidades Anticipadas (Arriendos/Ahorro)", font=("Arial", 12, "bold")).pack(pady=10)

        box_basic = ttk.LabelFrame(self, text="Datos de la Operación", padding=10)
        box_basic.pack(fill="x", pady=5)
        
        ttk.Label(box_basic, text="Valor Base ($):").pack(side="left", padx=5)
        self.base_var = tk.StringVar(value="1000000")
        ttk.Entry(box_basic, textvariable=self.base_var).pack(side="left", padx=5)

        ttk.Label(box_basic, text="Plazo (años):").pack(side="left", padx=5)
        self.years_var = tk.StringVar(value="1")
        ttk.Entry(box_basic, textvariable=self.years_var).pack(side="left", padx=5)

        self.rate_frame = RateInputFrame(self)
        self.rate_frame.pack(fill="x", pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Calcular Canon/Cuota (Arriendo)", command=self.calc_cuota).pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="Calcular Valor Presente (Deuda)", command=self.calc_vp).pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="Calcular Ahorro Total (Futuro)", command=self.calc_vf).pack(side="left", expand=True, padx=2)

        self.result_lbl = ttk.Label(self, text="", font=("Arial", 11, "bold"))
        self.result_lbl.pack(pady=10)

    def _get_validated_data(self):
        rate_data = self.rate_frame.get_values()
        return {
            "base": validate_number(self.base_var.get(), "Valor Base"),
            "years": validate_number(self.years_var.get(), "Plazo"),
            "rate": validate_number(rate_data["rate"], "Tasa"),
            "tipo_tasa": rate_data["tipo_tasa"],
            "periodo_tasa": rate_data["periodo_tasa"],
            "periodicidad": rate_data["periodicidad"]
        }

    def calc_cuota(self):
        try:
            d = self._get_validated_data()
            val = self.controller.annuity_payment(d['base'], d['rate'], d['tipo_tasa'], d['periodo_tasa'], d['years'], d['periodicidad'])
            self.result_lbl.config(text=f"Cuota Anticipada (Canon): ${val:,.2f}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def calc_vp(self):
        try:
            d = self._get_validated_data()
            val = self.controller.annuity_pv(d['base'], d['rate'], d['tipo_tasa'], d['periodo_tasa'], d['years'], d['periodicidad'])
            self.result_lbl.config(text=f"Valor Presente (Total Contrato): ${val:,.2f}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def calc_vf(self):
        try:
            d = self._get_validated_data()
            val = self.controller.annuity_fv(d['base'], d['rate'], d['tipo_tasa'], d['periodo_tasa'], d['years'], d['periodicidad'])
            self.result_lbl.config(text=f"Ahorro Total Acumulado: ${val:,.2f}")
        except Exception as e: messagebox.showerror("Error", str(e))