# ============================================================
#  Tax Calculator — Multi-Country
#  Supports: Pakistan, USA, UK, UAE, Canada
# ============================================================

TAX_SYSTEMS = {
    "1": {
        "name": "Pakistan (FBR 2024)",
        "currency": "PKR",
        "brackets": {
            "single": [
                (0,        600_000,   0.00),
                (600_000,  1_200_000, 0.05),
                (1_200_000,2_400_000, 0.15),
                (2_400_000,3_600_000, 0.25),
                (3_600_000,6_000_000, 0.30),
                (6_000_000,float("inf"), 0.35),
            ]
        },
    },
    "2": {
        "name": "USA (Federal 2024)",
        "currency": "USD",
        "brackets": {
            "single": [
                (0,       11_600,  0.10),
                (11_600,  47_150,  0.12),
                (47_150,  100_525, 0.22),
                (100_525, 191_950, 0.24),
                (191_950, 243_725, 0.32),
                (243_725, 609_350, 0.35),
                (609_350, float("inf"), 0.37),
            ],
            "married": [
                (0,       23_200,  0.10),
                (23_200,  94_300,  0.12),
                (94_300,  201_050, 0.22),
                (201_050, 383_900, 0.24),
                (383_900, 487_450, 0.32),
                (487_450, 731_200, 0.35),
                (731_200, float("inf"), 0.37),
            ],
        },
    },
    "3": {
        "name": "UK (HMRC 2024)",
        "currency": "GBP",
        "brackets": {
            "single": [
                (0,       12_570,  0.00),
                (12_570,  50_270,  0.20),
                (50_270,  125_140, 0.40),
                (125_140, float("inf"), 0.45),
            ]
        },
    },
    "4": {
        "name": "UAE",
        "currency": "AED",
        "brackets": {
            "single": [
                (0, float("inf"), 0.00),
            ]
        },
    },
    "5": {
        "name": "Canada (Federal 2024)",
        "currency": "CAD",
        "brackets": {
            "single": [
                (0,       55_867,  0.15),
                (55_867,  111_733, 0.205),
                (111_733, 154_906, 0.26),
                (154_906, 220_000, 0.29),
                (220_000, float("inf"), 0.33),
            ]
        },
    },
}


def calculate_tax(income, brackets):
    """Calculate tax using progressive bracket system."""
    total_tax = 0
    details = []

    for low, high, rate in brackets:
        if income <= low:
            break
        taxable = min(income, high) - low
        tax = taxable * rate
        total_tax += tax
        details.append((low, high, rate, taxable, tax))

    return total_tax, details


def fmt(amount, currency):
    """Format a number as currency string."""
    return f"{currency} {amount:,.2f}"


def print_separator(char="─", width=55):
    print(char * width)


def print_bracket_table(details, currency):
    """Print a formatted bracket breakdown table."""
    SEP = "  " + "─" * 65
    print(f"\n  {'Bracket':<30} {'Rate':>5}  {'Taxable':>14}  {'Tax':>14}")
    print(SEP)

    for i, (low, high, rate, taxable, tax) in enumerate(details):
        high_str = "above     " if high == float("inf") else f"{high:>12,.0f}"
        bracket_label = f"{low:>12,.0f} – {high_str}"
        marker = " ◀" if i == len(details) - 1 else "  "
        print(f"  {bracket_label:<30} {rate*100:>4.0f}%  {taxable:>14,.2f}  {tax:>14,.2f}{marker}")

    print(SEP)


def run_calculator():
    print()
    print_separator("═")
    print("  💰  INCOME TAX CALCULATOR  —  Multi-Country")
    print_separator("═")

    # --- Country selection ---
    print("\n  Select a country:")
    for key, system in TAX_SYSTEMS.items():
        print(f"    [{key}] {system['name']}")

    while True:
        choice = input("\n  Enter number (1–5): ").strip()
        if choice in TAX_SYSTEMS:
            break
        print("  ⚠  Invalid choice. Please enter a number from 1 to 5.")

    system = TAX_SYSTEMS[choice]
    currency = system["currency"]
    has_married = "married" in system["brackets"]

    # --- Filing status ---
    if has_married:
        print("\n  Filing status:")
        print("    [1] Single / Individual")
        print("    [2] Married / Joint")
        while True:
            s = input("\n  Enter choice (1 or 2): ").strip()
            if s == "1":
                status = "single"
                break
            elif s == "2":
                status = "married"
                break
            print("  ⚠  Please enter 1 or 2.")
    else:
        status = "single"

    brackets = system["brackets"][status]

    # --- Income input ---
    while True:
        try:
            income_str = input(f"\n  Enter annual income ({currency}): ").strip().replace(",", "")
            income = float(income_str)
            if income < 0:
                print("  ⚠  Income cannot be negative.")
                continue
            break
        except ValueError:
            print("  ⚠  Please enter a valid number.")

    # --- Calculate ---
    total_tax, details = calculate_tax(income, brackets)
    take_home = income - total_tax
    effective_rate = (total_tax / income * 100) if income > 0 else 0
    marginal_rate = details[-1][2] * 100 if details else 0

    # --- Output ---
    print()
    print_separator("═")
    print(f"  📊  TAX SUMMARY  —  {system['name']}")
    print_separator("═")
    print(f"\n  Gross Income       {fmt(income, currency):>22}")
    print(f"  Total Tax          {fmt(total_tax, currency):>22}")
    print(f"  Take-Home Pay      {fmt(take_home, currency):>22}")
    print(f"\n  Effective Tax Rate          {effective_rate:>8.2f}%")
    print(f"  Marginal Tax Rate           {marginal_rate:>8.2f}%")
    print(f"  Monthly Take-Home  {fmt(take_home / 12, currency):>22}")

    if details:
        print(f"\n{'─'*55}")
        print("  BRACKET BREAKDOWN")
        print_bracket_table(details, currency)
        print("  ◀  Your highest bracket")

    print()
    print_separator("═")


def main():
    while True:
        run_calculator()
        again = input("  Calculate again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye! 👋\n")
            break


if __name__ == "__main__":
    main()