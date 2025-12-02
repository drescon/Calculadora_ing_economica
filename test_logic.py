from app.models.calculator import CreditCalculator

def test_calculator():
    calc = CreditCalculator()
    
    # Test Case 1: $10,000, 12% annual, 1 year, Monthly
    # Rate per period = 1% (0.01)
    # Periods = 12
    # PMT = 10000 * (0.01 * 1.01^12) / (1.01^12 - 1) = 888.49
    
    result = calc.calculate_amortization(10000, 12, 1, "Mensual")
    print("Test Case 1 (Monthly):")
    print(f"Installment: {result['installment']}")
    print(f"Total Interest: {result['total_interest']}")
    print(f"Total Payment: {result['total_payment']}")
    
    assert abs(result['installment'] - 888.49) < 0.05, f"Expected ~888.49, got {result['installment']}"
    
    # Check if balance goes to 0
    final_balance = result['schedule'][-1]['Saldo']
    print(f"Final Balance: {final_balance}")
    assert final_balance == 0, f"Expected final balance 0, got {final_balance}"

    # Test Case 2: $10,000, 12% annual, 1 year, Quarterly
    # Rate per period = 3% (0.03)
    # Periods = 4
    # PMT = 10000 * (0.03 * 1.03^4) / (1.03^4 - 1) = 2690.27
    
    result = calc.calculate_amortization(10000, 12, 1, "Trimestral")
    print("\nTest Case 2 (Quarterly):")
    print(f"Installment: {result['installment']}")
    
    assert abs(result['installment'] - 2690.27) < 0.05, f"Expected ~2690.27, got {result['installment']}"

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_calculator()
