import tkinter as tk
from tkinter import ttk, messagebox
from app.views.components.rate_input_frame import RateInputFrame
from app.utils.tasa_utils import convert_to_period_rate, PERIODS_PER_YEAR
from app.utils.validators import validate_number


class CapitalizationFrame(ttk.Frame):
    """Tab for calculating future value of periodic savings with compound interest.
    The user provides:
      * Ahorro mensual (contribution per period)
      * Número de meses
      * Tasa de interés (via RateInputFrame)
      * Periodicidad de capitalización (mensual, trimestral, semestral, anual)
    """

    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Calculadora de Capitalización (Interés Compuesto)",
                  font=("Arial", 12, "bold")).pack(pady=10)

        # Frame for basic inputs
        box_basic = ttk.LabelFrame(self, text="Datos de la Aportación", padding=10)
        box_basic.pack(fill="x", pady=5)

        # Ahorro mensual
        ttk.Label(box_basic, text="Ahorro mensual ($):").pack(side="left", padx=5)
        self.aportacion_var = tk.StringVar(value="1000")
        ttk.Entry(box_basic, textvariable=self.aportacion_var, width=12).pack(side="left", padx=5)

        # Número de años
        ttk.Label(box_basic, text="Años:").pack(side="left", padx=5)
        self.anos_var = tk.StringVar(value="1")
        ttk.Entry(box_basic, textvariable=self.anos_var, width=6).pack(side="left", padx=5)

        # Rate input (interest rate, type, period, capitalization frequency)
        self.rate_frame = RateInputFrame(self)
        self.rate_frame.pack(fill="x", pady=10)

        # Button to calculate future value
        btn = ttk.Button(self, text="Calcular Valor Futuro", command=self.calc_fv)
        btn.pack(pady=5)

        # Result label
        self.result_lbl = ttk.Label(self, text="", font=("Arial", 11, "bold"))
        # Table for progress over time
        self.table = ttk.Treeview(self, columns=("period", "aporte", "interes", "saldo"), show="headings")
        for col, txt in [("period", "Periodo"), ("aporte", "Aporte"), ("interes", "Interés"), ("saldo", "Saldo")]:
            self.table.heading(col, text=txt)
            self.table.column(col, width=80, anchor="e")
        self.table.pack(fill="both", expand=True, pady=5)
        self.result_lbl.pack(pady=10)

    def _get_validated_data(self):
        # Validate numeric inputs
        aporte = validate_number(self.aportacion_var.get(), "Ahorro mensual")
        anos = validate_number(self.anos_var.get(), "Años")
        # Get rate data from RateInputFrame
        rate_data = self.rate_frame.get_values()
        return {
            "aporte": aporte,
            "anos": anos,
            "rate": validate_number(rate_data["rate"], "Tasa"),
            "tipo_tasa": rate_data["tipo_tasa"],
            "periodo_tasa": rate_data["periodo_tasa"],
            "periodicidad": rate_data["periodicidad"]
        }

    def calc_fv(self):
        # Clear previous results first
        self.result_lbl.config(text="")
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            d = self._get_validated_data()
            # Use years directly
            years = d["anos"]
            fv = self.controller.annuity_fv(
                base=d["aporte"],
                rate=d["rate"],
                tipo=d["tipo_tasa"],
                p_tasa=d["periodo_tasa"],
                years=years,
                p_pago=d["periodicidad"]
            )
            
            # Get schedule
            schedule = self.controller.get_capitalization_schedule(
                aporte=d["aporte"],
                rate=d["rate"],
                tipo=d["tipo_tasa"],
                p_tasa=d["periodo_tasa"],
                years=years,
                p_pago=d["periodicidad"]
            )
            
            # Populate table
            for row in schedule:
                self.table.insert("", "end", values=(
                    row["period"],
                    f"${row['aporte']:,.2f}",
                    f"${row['interes']:,.2f}",
                    f"${row['saldo']:,.2f}"
                ))

            self.result_lbl.config(
                text=f"Resultado: Ahorrando ${d['aporte']:,.2f} al mes durante {d['anos']} años,\n" 
                     f"obtenerás un valor futuro de ${fv:,.2f}."
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
