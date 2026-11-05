"""Rate card and payment functions for the village milk co-operative."""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")
MIN_SNF = Decimal("0.0")       # Assumption: SNF cannot be negative.
MAX_SNF = Decimal("20.0")      # Assumption: practical validation ceiling.
CENT = Decimal("0.01")
STEP = Decimal("0.1")


def round_money(value):
    """Round a monetary value to the nearest paisa."""
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def step_count(value, standard):
    """Count 0.1 percentage-point steps, rounding half steps away from zero."""
    difference = Decimal(value) - Decimal(standard)
    return int((difference / STEP).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rate_per_litre(fat, snf, season="regular"):
    """Return the applicable rate per litre, rounded to two decimals."""
    fat = Decimal(str(fat))
    snf = Decimal(str(snf))
    if not (MIN_FAT <= fat <= MAX_FAT):
        raise ValueError(f"Fat must be between {MIN_FAT} and {MAX_FAT}.")
    if not (MIN_SNF <= snf <= MAX_SNF):
        raise ValueError(f"SNF must be between {MIN_SNF} and {MAX_SNF}.")

    if season == "april_june":
        base = Decimal("32.00")
        fat_value = Decimal("0.45")
    elif season == "regular":
        base = BASE_RATE
        fat_value = FAT_STEP_VALUE
    else:
        raise ValueError("Season must be 'regular' or 'april_june'.")

    fat_steps = step_count(fat, STANDARD_FAT)
    snf_steps = step_count(snf, STANDARD_SNF)
    return round_money(base + fat_steps * fat_value + snf_steps * SNF_STEP_VALUE)


def bonus_amount(litres, threshold=Decimal("500"), bonus_rate=Decimal("0.50")):
    """Bonus is paid on every litre if the ten-day volume is strictly above 500 L."""
    litres = Decimal(str(litres))
    return round_money(litres * bonus_rate) if litres > threshold else Decimal("0.00")


def payout(litres, fat, snf, season="regular"):
    """Calculate one entry's payment, rounded to the nearest paisa."""
    litres = Decimal(str(litres))
    if litres < 0:
        raise ValueError("Litres cannot be negative.")
    rate = rate_per_litre(fat, snf, season)
    return round_money(litres * rate)


def ten_day_total(entries, season="regular"):
    """Return (milk_total, base_pay_total, bonus, final_total)."""
    milk_total = sum((Decimal(str(e["litres"])) for e in entries), Decimal("0"))
    base_pay = sum((payout(e["litres"], e["fat"], e["snf"], season)
                    for e in entries), Decimal("0.00"))
    bonus = bonus_amount(milk_total)
    return milk_total, round_money(base_pay), bonus, round_money(base_pay + bonus)
