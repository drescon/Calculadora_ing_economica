from app.models.calculator import CreditCalculator
from app.views.main_window import MainWindow

class MainController:
    def __init__(self):
        self.model = CreditCalculator()
        self.view = MainWindow(self)

    def run(self):
        self.view.mainloop()

    def calculate(self, amount, rate, years, periodicity):
        """
        Called by the view when the calculate button is clicked.
        """
        try:
            result = self.model.calculate_amortization(amount, rate, years, periodicity)
            self.view.update_results(
                result['installment'],
                result['total_interest'],
                result['schedule']
            )
        except ValueError as e:
            # In a real app, you might want to pass this error back to the view to display
            print(f"Error: {e}")
