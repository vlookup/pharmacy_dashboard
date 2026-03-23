import csv
import random
import os
from datetime import datetime, timedelta

# -----------------------------------------
# Resolve project root and output path
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE_DIR, "data_raw", "claims.csv")

# -----------------------------------------
# Configuration
# -----------------------------------------
random.seed(42)

N_CLAIMS = 100000
PHARMACY_TYPES = ["Retail", "Mail", "Specialty"]

# 12-month window
END_DATE = datetime.today()
START_DATE = END_DATE - timedelta(days=365)

# -----------------------------------------
# Load customers and drugs
# -----------------------------------------
def load_csv(path):
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

CUSTOMERS = load_csv(os.path.join(BASE_DIR, "data_raw", "customers.csv"))
DRUGS = load_csv(os.path.join(BASE_DIR, "data_raw", "drugs.csv"))

# -----------------------------------------
# Claim generator
# -----------------------------------------
def generate_claim(claim_id: int):
    customer = random.choice(CUSTOMERS)
    drug = random.choice(DRUGS)

    # Random fill date in last 12 months
    days_offset = random.randint(0, 365)
    fill_date = (START_DATE + timedelta(days=days_offset)).strftime("%Y-%m-%d")

    quantity = random.choice([30, 60, 90])
    days_supply = quantity  # simple alignment

    unit_cost = float(drug["unit_cost"])
    total_cost = round(unit_cost * (quantity / 30), 2)

    # Cost split
    member_paid = round(total_cost * random.uniform(0.05, 0.25), 2)
    plan_paid = round(total_cost - member_paid, 2)

    pharmacy_type = random.choices(
        PHARMACY_TYPES,
        weights=[0.70, 0.20, 0.10],  # mostly retail
        k=1
    )[0]

    return {
        "claim_id": f"CL{claim_id:06d}",
        "customer_id": customer["customer_id"],
        "drug_id": drug["drug_id"],
        "ndc": drug["ndc"],
        "fill_date": fill_date,
        "quantity": quantity,
        "days_supply": days_supply,
        "pharmacy_type": pharmacy_type,
        "total_cost": total_cost,
        "plan_paid": plan_paid,
        "member_paid": member_paid,
    }

# -----------------------------------------
# Main writer
# -----------------------------------------
def main():
    fieldnames = [
        "claim_id",
        "customer_id",
        "drug_id",
        "ndc",
        "fill_date",
        "quantity",
        "days_supply",
        "pharmacy_type",
        "total_cost",
        "plan_paid",
        "member_paid",
    ]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, N_CLAIMS + 1):
            writer.writerow(generate_claim(i))

    print(f"Wrote {N_CLAIMS} claims to {output_path}")

# -----------------------------------------
# Entry point
# -----------------------------------------
if __name__ == "__main__":
    main()