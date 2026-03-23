import csv
import random
import os

# -----------------------------------------
# Resolve project root and output path
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(BASE_DIR, "data_raw", "drugs.csv")

# -----------------------------------------
# Configuration
# -----------------------------------------
random.seed(42)

N_DRUGS = 500

THERAPEUTIC_CLASSES = {
    "Diabetes": ["Metformin", "Glipizide", "Januvia", "Ozempic", "Trulicity"],
    "Cardiovascular": ["Lisinopril", "Amlodipine", "Atorvastatin", "Metoprolol", "Eliquis"],
    "Mental Health": ["Sertraline", "Fluoxetine", "Bupropion", "Abilify", "Seroquel"],
    "Pain Management": ["Ibuprofen", "Naproxen", "Celebrex", "Tramadol", "Oxycodone"],
    "Autoimmune": ["Humira", "Enbrel", "Stelara", "Cosentyx", "Xeljanz"],
    "Respiratory": ["Albuterol", "Advair", "Symbicort", "Montelukast", "Spiriva"],
    "GI": ["Omeprazole", "Pantoprazole", "Linzess", "Trulance", "Mesalamine"],
    "Oncology": ["Imbruvica", "Revlimid", "Ibrance", "Keytruda", "Opdivo"],
}

BRAND_PROBABILITY = 0.35  # 35% brand, 65% generic

# -----------------------------------------
# Helper functions
# -----------------------------------------
def generate_ndc():
    """Generate a synthetic 10-digit NDC-like code."""
    return f"{random.randint(10000,99999)}-{random.randint(1000,9999)}-{random.randint(10,99)}"

def generate_unit_cost(is_brand, therapeutic_class):
    """Generate realistic unit costs by class and brand/generic."""
    base_ranges = {
        "Diabetes": (5, 600),
        "Cardiovascular": (3, 150),
        "Mental Health": (4, 300),
        "Pain Management": (2, 200),
        "Autoimmune": (500, 6000),
        "Respiratory": (10, 400),
        "GI": (5, 350),
        "Oncology": (1000, 12000),
    }

    low, high = base_ranges[therapeutic_class]

    # Generic drugs are cheaper
    if not is_brand:
        high = max(low + 5, high * 0.25)

    return round(random.uniform(low, high), 2)

# -----------------------------------------
# Drug generator
# -----------------------------------------
def generate_drug(drug_id: int):
    therapeutic_class = random.choice(list(THERAPEUTIC_CLASSES.keys()))
    drug_name = random.choice(THERAPEUTIC_CLASSES[therapeutic_class])

    is_brand = 1 if random.random() < BRAND_PROBABILITY else 0
    ndc = generate_ndc()
    unit_cost = generate_unit_cost(is_brand, therapeutic_class)

    return {
        "drug_id": f"D{drug_id:04d}",
        "drug_name": drug_name,
        "ndc": ndc,
        "therapeutic_class": therapeutic_class,
        "brand_flag": is_brand,
        "unit_cost": unit_cost,
    }

# -----------------------------------------
# Main writer
# -----------------------------------------
def main():
    fieldnames = [
        "drug_id",
        "drug_name",
        "ndc",
        "therapeutic_class",
        "brand_flag",
        "unit_cost",
    ]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, N_DRUGS + 1):
            writer.writerow(generate_drug(i))

    print(f"Wrote {N_DRUGS} drugs to {output_path}")

# -----------------------------------------
# Entry point
# -----------------------------------------
if __name__ == "__main__":
    main()