from app.models.calculator import CreditCalculator
from app.views.main_window import MainWindow

class MainController:
    def __init__(self):
        self.model = CreditCalculator()
        self.view = MainWindow(self)

    def run(self):
        self.view.mainloop()

    def calculate(self, mode, amount, rate, tipo_tasa, periodo_tasa,
                  years, periodicidad, cuota_input=None):
        try:
            if mode == "calcular_cuota":
                result = self.model.amortizacion_francesa(
                    principal=amount, rate_percent=rate, tipo_tasa=tipo_tasa,
                    periodo_tasa=periodo_tasa, years=years, periodicidad_pago=periodicidad
                )
                self.view.credit_tab.update_results(
                    result["installment"], result["total_interest"], result["schedule"],
                    result["total_payment"], result["periods"]
                )

            elif mode == "calcular_monto":
                monto = self.model.compute_max_amount_from_installment(
                    installment_input=cuota_input, rate_percent=rate, tipo_tasa=tipo_tasa,
                    periodo_tasa=periodo_tasa, years=years, periodicidad_pago=periodicidad
                )
                result = self.model.amortizacion_francesa(
                    principal=monto, rate_percent=rate, tipo_tasa=tipo_tasa,
                    periodo_tasa=periodo_tasa, years=years, periodicidad_pago=periodicidad
                )
                self.view.credit_tab.update_results(
                    result["installment"], result["total_interest"], result["schedule"],
                    result["total_payment"], result["periods"], computed_amount=monto
                )
            else:
                self.view.credit_tab.show_error("Modo inválido.")

        except Exception as e:
            self.view.credit_tab.show_error(f"Error en controlador: {str(e)}")

    def calculate_compound_fv(self, pv_or_fv, rate, tipo_tasa, periodo_tasa, years, periodicidad):
        return self.model.future_value(pv_or_fv, rate, tipo_tasa, periodo_tasa, years, periodicidad)

    def calculate_compound_pv(self, pv_or_fv, rate, tipo_tasa, periodo_tasa, years, periodicidad):
        return self.model.present_value(pv_or_fv, rate, tipo_tasa, periodo_tasa, years, periodicidad)

    def annuity_payment(self, base, rate, tipo, p_tasa, years, p_pago):
        return self.model.annuity_due_payment_from_present(base, rate, tipo, p_tasa, years, p_pago)

    def annuity_pv(self, base, rate, tipo, p_tasa, years, p_pago):
        return self.model.annuity_due_present_from_payment(base, rate, tipo, p_tasa, years, p_pago)

    def annuity_fv(self, base, rate, tipo, p_tasa, years, p_pago):
        return self.model.annuity_due_future_from_payment(base, rate, tipo, p_tasa, years, p_pago)

    def get_capitalization_schedule(self, aporte, rate, tipo, p_tasa, years, p_pago):
        return self.model.capitalization_schedule(aporte, rate, tipo, p_tasa, years, p_pago)