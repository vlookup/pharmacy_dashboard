import csv
import random
import os

# -----------------------------------------
# Resolve project root and output path
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE_DIR, "data_raw", "customers.csv")

# -----------------------------------------
# Configuration
# -----------------------------------------
random.seed(42)

N_CUSTOMERS = 1000
REGIONS = ["Northeast", "Midwest", "South", "West"]
PLAN_TYPES = ["Bronze", "Silver", "Gold", "Platinum"]
GENDERS = ["M", "F"]

# -----------------------------------------
# Customer generator
# -----------------------------------------
def generate_customer(customer_id: int):
    cid = f"C{customer_id:04d}"
    age = random.randint(18, 90)
    gender = random.choice(GENDERS)
    region = random.choice(REGIONS)
    plan_type = random.choices(
        PLAN_TYPES,
        weights=[0.25, 0.35, 0.30, 0.10],  # more Bronze/Silver, fewer Platinum
        k=1
    )[0]

    # Base risk by age
    base_risk = 0.3 + (age - 18) / 100.0
    risk_score = round(base_risk + random.uniform(-0.2, 1.5), 2)
    risk_score = max(0.1, min(risk_score, 3.5))

    # Condition flags
    diabetes_flag = 1 if (age > 45 and random.random() < 0.30) else 0
    cvd_flag = 1 if (age > 50 and random.random() < 0.35) else 0
    mental_health_flag = 1 if random.random() < 0.25 else 0
    respiratory_flag = 1 if random.random() < 0.20 else 0
    gi_flag = 1 if random.random() < 0.15 else 0

    return {
        "customer_id": cid,
        "age": age,
        "gender": gender,
        "region": region,
        "plan_type": plan_type,
        "risk_score": risk_score,
        "diabetes_flag": diabetes_flag,
        "cvd_flag": cvd_flag,
        "mental_health_flag": mental_health_flag,
        "respiratory_flag": respiratory_flag,
        "gi_flag": gi_flag,
    }

# -----------------------------------------
# Main writer
# -----------------------------------------
def main():
    fieldnames = [
        "customer_id",
        "age",
        "gender",
        "region",
        "plan_type",
        "risk_score",
        "diabetes_flag",
        "cvd_flag",
        "mental_health_flag",
        "respiratory_flag",
        "gi_flag",
    ]

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, N_CUSTOMERS + 1):
            writer.writerow(generate_customer(i))

    print(f"Wrote {N_CUSTOMERS} customers to {output_path}")

# -----------------------------------------
# Entry point
# -----------------------------------------
if __name__ == "__main__":
    main()