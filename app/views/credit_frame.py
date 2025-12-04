import tkinter as tk
from tkinter import ttk, messagebox
from app.views.credit_inputs_frame import CreditInputsFrame
from app.views.amortization_schedule import AmortizationSchedule
from app.utils.validators import validate_number

class CreditFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        self.mode_var = tk.StringVar(value="calcular_cuota") 
        self._build_ui()
        self.mode_var.trace_add("write", lambda *args: self._update_mode())

    def _build_ui(self):
        top = ttk.LabelFrame(self, text="Opciones de Cálculo", padding=10)
        top.pack(fill="x")

        ttk.Radiobutton(top, text="Calcular cuota (usando monto)", variable=self.mode_var,
                        value="calcular_cuota").pack(side="left", padx=5)

        ttk.Radiobutton(top, text="Calcular monto (usando cuota)", variable=self.mode_var,
                        value="calcular_monto").pack(side="left", padx=5)

        self.inputs_frame = CreditInputsFrame(self)
        self.inputs_frame.pack(fill="x", pady=10)

        self.schedule_frame = AmortizationSchedule(self) 
        self.schedule_frame.pack(fill="both", expand=True)

        self._create_buttons() 
        self._update_mode()

    def _create_buttons(self):
        box = ttk.Frame(self, padding=5)
        box.pack(fill="x")
        ttk.Button(box, text="Calcular", command=self.on_calculate).pack(side="left", padx=5)
        ttk.Button(box, text="Limpiar tabla", command=self.schedule_frame.clear_table).pack(side="left", padx=5)

    def _update_mode(self):
        mode = self.mode_var.get()
        self.inputs_frame.set_mode(mode)
        if mode == "calcular_cuota":
            self.schedule_frame.monto_lbl.config(text="")
        else:
            self.schedule_frame.monto_lbl.config(text="Cálculo de monto máximo")

    def on_calculate(self):
        try:
            mode = self.mode_var.get()
            raw = self.inputs_frame.get_data()
            
            validated_data = {
                "mode": mode,
                "amount": validate_number(raw["amount"], "Monto", must_be_positive=False),
                "cuota_input": validate_number(raw["cuota_input"], "Cuota", must_be_positive=False),
                "years": validate_number(raw["years"], "Plazo"),
                "rate": validate_number(raw["rate"], "Tasa"),
                "tipo_tasa": raw["tipo_tasa"],
                "periodo_tasa": raw["periodo_tasa"],
                "periodicidad": raw["periodicidad"]
            }

            if mode == "calcular_cuota":
                if validated_data["amount"] <= 0: raise ValueError("El Monto debe ser positivo.")
                validated_data["cuota_input"] = 0
            elif mode == "calcular_monto":
                if validated_data["cuota_input"] <= 0: raise ValueError("La Cuota debe ser positiva.")
                validated_data["amount"] = 0

            self.controller.calculate(**validated_data)
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def update_results(self, installment, total_interest, schedule, total_payment, periods, computed_amount=None):
        self.schedule_frame.update_results(installment, total_interest, schedule, total_payment, periods, computed_amount)