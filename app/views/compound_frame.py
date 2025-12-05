import tkinter as tk
from tkinter import ttk, messagebox
from app.views.components.rate_input_frame import RateInputFrame
from app.utils.validators import validate_number

class CompoundFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Simulador de Inversión (Interés Compuesto)", font=("Arial", 12, "bold")).pack(pady=10)

        box_basic = ttk.LabelFrame(self, text="Datos de la Inversión / Ahorro", padding=10)
        box_basic.pack(fill="x", pady=5)
        
        ttk.Label(box_basic, text="Monto ($):").pack(side="left", padx=5)
        self.monto_var = tk.StringVar(value="1000000")
        ttk.Entry(box_basic, textvariable=self.monto_var).pack(side="left", padx=5)

        ttk.Label(box_basic, text="Plazo (años):").pack(side="left", padx=5)
        self.years_var = tk.StringVar(value="1")
        ttk.Entry(box_basic, textvariable=self.years_var).pack(side="left", padx=5)

        self.rate_frame = RateInputFrame(self)
        self.rate_frame.pack(fill="x", pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="¿Cuánto tendré? (Calcular Valor Futuro)", command=self.calc_fv).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(btn_frame, text="¿Cuánto invertir hoy? (Calcular Meta de Ahorro)", command=self.calc_pv).pack(side="left", expand=True, fill="x", padx=5)

        self.result_lbl = ttk.Label(self, text="", font=("Arial", 11, "bold"))
        self.result_lbl.pack(pady=10)

    def _get_validated_data(self):
        rate_data = self.rate_frame.get_values()
        return {
            "pv_or_fv": validate_number(self.monto_var.get(), "Monto"),
            "years": validate_number(self.years_var.get(), "Plazo"),
            "rate": validate_number(rate_data["rate"], "Tasa"),
            "tipo_tasa": rate_data["tipo_tasa"],
            "periodo_tasa": rate_data["periodo_tasa"],
            "periodicidad": rate_data["periodicidad"]
        }

    def calc_fv(self):
        try:
            d = self._get_validated_data()
            vf = self.controller.calculate_compound_fv(d["pv_or_fv"], d["rate"], d["tipo_tasa"], d["periodo_tasa"], d["years"], d["periodicidad"])
            self.result_lbl.config(text=f"Resultado: Si inviertes ${d['pv_or_fv']:,.2f} hoy,\ntendrás ${vf:,.2f} al final del plazo.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def calc_pv(self):
        try:
            d = self._get_validated_data()
            vp = self.controller.calculate_compound_pv(d["pv_or_fv"], d["rate"], d["tipo_tasa"], d["periodo_tasa"], d["years"], d["periodicidad"])
            self.result_lbl.config(text=f"Resultado: Para obtener ${d['pv_or_fv']:,.2f} en el futuro,\ndebes invertir hoy: ${vp:,.2f}")
        except Exception as e: messagebox.showerror("Error", str(e))