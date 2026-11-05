"""Clerk-facing milk payment calculator."""
from decimal import Decimal, InvalidOperation
from milkrate import rate_per_litre, payout, ten_day_total, MIN_FAT, MAX_FAT, MIN_SNF, MAX_SNF


def read_decimal(prompt, minimum=None, maximum=None):
    """Read and validate a decimal number from the keyboard."""
    while True:
        raw = input(prompt).strip()
        try:
            value = Decimal(raw)
        except InvalidOperation:
            print("Invalid number. Enter digits, optionally with a decimal point.")
            continue
        if not value.is_finite():
            print("Enter a finite number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Value must not exceed {maximum}.")
            continue
        return value


def collect_entries():
    entries = []
    count = int(read_decimal("Number of milk entries: ", Decimal("1"), Decimal("10000")))
    for index in range(1, count + 1):
        print(f"\\nEntry {index}")
        farmer_id = input("Farmer ID: ").strip()
        while not farmer_id:
            print("Farmer ID cannot be empty.")
            farmer_id = input("Farmer ID: ").strip()
        shift = input("Shift (morning/evening): ").strip().lower()
        while shift not in ("morning", "evening"):
            print("Enter morning or evening.")
            shift = input("Shift (morning/evening): ").strip().lower()
        litres = read_decimal("Litres: ", Decimal("0"))
        fat = read_decimal("Fat % (2.0 to 7.0): ", MIN_FAT, MAX_FAT)
        snf = read_decimal("SNF % (0.0 to 20.0): ", MIN_SNF, MAX_SNF)
        entries.append({"farmer_id": farmer_id, "shift": shift,
                        "litres": litres, "fat": fat, "snf": snf})
    return entries


def main():
    print("Ksheera Village Milk Producers' Co-operative")
    season = input("Season (regular/april_june): ").strip().lower()
    while season not in ("regular", "april_june"):
        print("Enter regular or april_june.")
        season = input("Season (regular/april_june): ").strip().lower()

    entries = collect_entries()
    print("\\nPAYMENT DETAILS")
    for entry in entries:
        rate = rate_per_litre(entry["fat"], entry["snf"], season)
        amount = payout(entry["litres"], entry["fat"], entry["snf"], season)
        print(f'{entry["farmer_id"]:12} {entry["shift"]:8} '
              f'{entry["litres"]:>8} L  rate Rs.{rate:>6}  amount Rs.{amount:>9}')

    litres, base_pay, bonus, final_total = ten_day_total(entries, season)
    print("\\nTEN-DAY SUMMARY")
    print(f"Total litres : {litres}")
    print(f"Milk payment: Rs. {base_pay:.2f}")
    print(f"Volume bonus: Rs. {bonus:.2f}")
    print(f"Final total : Rs. {final_total:.2f}")


if __name__ == "__main__":
    main()
