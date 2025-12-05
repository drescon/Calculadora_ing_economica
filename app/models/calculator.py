import math
from app.utils.tasa_utils import convert_to_period_rate, PERIODS_PER_YEAR

class CreditCalculator:
    def __init__(self):
        self.periodicity_map = PERIODS_PER_YEAR.copy()

    def _rate_per_period(self, rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago, momento="Vencida"):
        return convert_to_period_rate(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago, momento)

    def amortizacion_francesa(self, principal, rate_percent, tipo_tasa, periodo_tasa,
                              years, periodicidad_pago, momento="Vencida"):
        if periodicidad_pago not in self.periodicity_map:
            raise ValueError("Periodicidad inválida.")
        
        periods_per_year = self.periodicity_map[periodicidad_pago]
        n = int(years * periods_per_year)
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago, momento)

        if n <= 0: raise ValueError("Plazo inválido.")

        if abs(i) < 1e-15:
            cuota = principal / n
        else:
            cuota = principal * (i * (1 + i)**n) / ((1 + i)**n - 1)

        schedule = []
        balance = principal
        total_interest = 0.0

        for period in range(1, n + 1):
            interest = balance * i
            principal_paid = cuota - interest
            
            if period == n: 
                principal_paid = balance
                cuota = interest + principal_paid

            balance = round(balance - principal_paid, 10)
            total_interest += interest

            schedule.append({
                "Periodo": period,
                "Cuota": round(cuota, 2),
                "Interés": round(interest, 2),
                "Amortización": round(principal_paid, 2),
                "Saldo": round(max(balance, 0.0), 2)
            })

        return {
            "installment": round(cuota, 2),
            "total_interest": round(total_interest, 2),
            "total_payment": round(principal + total_interest, 2),
            "schedule": schedule,
            "periods": n
        }

    def compute_max_amount_from_installment(self, installment_input, rate_percent, tipo_tasa,
                                            periodo_tasa, years, periodicidad_pago, momento="Vencida"):
        periods_per_year = self.periodicity_map[periodicidad_pago]
        n = int(years * periods_per_year)
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago, momento)

        if installment_input <= 0:
            raise ValueError("La cuota debe ser positiva.")

        if abs(i) < 1e-15:
            principal = installment_input * n
        else:
            principal = installment_input * ((1 + i)**n - 1) / (i * (1 + i)**n)

        return round(principal, 2)

    def future_value(self, pv, rate_percent, tipo_tasa, periodo_tasa, years, periodicidad_pago):
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago)
        n = int(years * self.periodicity_map[periodicidad_pago])
        return pv * (1 + i)**n

    def present_value(self, fv, rate_percent, tipo_tasa, periodo_tasa, years, periodicidad_pago):
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago)
        n = int(years * self.periodicity_map[periodicidad_pago])
        return fv / (1 + i)**n

    def annuity_due_payment_from_present(self, pv, rate_percent, tipo_tasa, periodo_tasa, years, periodicidad_pago):
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago)
        n = int(years * self.periodicity_map[periodicidad_pago])
        if abs(i) < 1e-15: return pv / n
        factor = ((1 - (1 + i)**(-n)) / i) * (1 + i)
        return pv / factor

    def annuity_due_present_from_payment(self, r, rate_percent, tipo_tasa, periodo_tasa, years, periodicidad_pago):
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago)
        n = int(years * self.periodicity_map[periodicidad_pago])
        if abs(i) < 1e-15: return r * n
        return r * ((1 - (1 + i)**(-n)) / i) * (1 + i)

    def annuity_due_future_from_payment(self, r, rate_percent, tipo_tasa, periodo_tasa, years, periodicidad_pago):
        i = self._rate_per_period(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago)
        n = int(years * self.periodicity_map[periodicidad_pago])
        if abs(i) < 1e-15: return r * n
        return r * (((1 + i)**n - 1) / i) * (1 + i)