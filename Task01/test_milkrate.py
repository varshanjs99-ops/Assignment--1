"""Repeatable tests for the payment calculator."""
from decimal import Decimal
from milkrate import rate_per_litre, payout, ten_day_total, bonus_amount

def run_tests():
    assert rate_per_litre("3.5", "8.5") == Decimal("30.00")
    assert rate_per_litre("4.2", "8.7") == Decimal("33.40")
    assert rate_per_litre("3.1", "8.3") == Decimal("27.80")
    assert payout("10", "3.5", "8.5") == Decimal("300.00")
    assert bonus_amount("500") == Decimal("0.00")
    assert bonus_amount("500.01") == Decimal("250.01")
    assert rate_per_litre("4.25", "8.5") == Decimal("33.20")
    try:
        rate_per_litre("7.1", "8.5")
    except ValueError:
        pass
    else:
        raise AssertionError("Fat validation failed")
    assert rate_per_litre("3.5", "8.5", "april_june") == Decimal("32.00")
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
