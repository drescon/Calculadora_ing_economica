import math

class CreditCalculator:
    def __init__(self):
        self.periodicity_map = {
            "Mensual": 12,
            "Trimestral": 4,
            "Semestral": 2,
            "Anual": 1
        }

    def calculate_amortization(self, principal, annual_rate, years, periodicity):
        """
        Calculates the amortization schedule.
        
        Args:
            principal (float): The loan amount.
            annual_rate (float): The annual interest rate (in percentage, e.g., 15 for 15%).
            years (int): The term of the loan in years.
            periodicity (str): The frequency of payments ("Mensual", "Trimestral", "Semestral", "Anual").
            
        Returns:
            dict: Contains 'installment', 'total_interest', 'total_payment', and 'schedule' (list of dicts).
        """
        if periodicity not in self.periodicity_map:
            raise ValueError(f"Invalid periodicity: {periodicity}")

        periods_per_year = self.periodicity_map[periodicity]
        n_periods = int(years * periods_per_year)
        rate_per_period = (annual_rate / 100) / periods_per_year

        if rate_per_period == 0:
            installment = principal / n_periods
        else:
            installment = principal * (rate_per_period * (1 + rate_per_period)**n_periods) / ((1 + rate_per_period)**n_periods - 1)

        schedule = []
        balance = principal
        total_interest = 0

        for period in range(1, n_periods + 1):
            interest = balance * rate_per_period
            principal_payment = installment - interest
            balance -= principal_payment
            
            # Handle floating point precision at the end
            if period == n_periods and abs(balance) < 0.01:
                principal_payment += balance
                balance = 0

            total_interest += interest
            
            schedule.append({
                "Periodo": period,
                "Cuota": round(installment, 2),
                "Interés": round(interest, 2),
                "Amortización": round(principal_payment, 2),
                "Saldo": round(max(0, balance), 2)
            })

        return {
            "installment": round(installment, 2),
            "total_interest": round(total_interest, 2),
            "total_payment": round(principal + total_interest, 2),
            "schedule": schedule
        }
