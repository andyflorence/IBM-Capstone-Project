"""
Space X Falcon 9 First Stage Landing Prediction
Lab 2: Data Wrangling

Performs Exploratory Data Analysis (EDA) and creates training labels
for supervised models predicting Falcon 9 first stage landing success.

Landing outcomes:
  - True Ocean / True RTLS / True ASDS  → successful landing  → Class = 1
  - False Ocean / False RTLS / False ASDS / None ASDS / None None → Class = 0
"""

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------------------------
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
)

df = pd.read_csv(DATA_URL)
print("=== First 10 rows ===")
print(df.head(10))


# ---------------------------------------------------------------------------
# 2. Exploratory Data Analysis
# ---------------------------------------------------------------------------

# Percentage of missing values per column
print("\n=== Missing values (%) ===")
print(df.isnull().sum() / len(df) * 100)

# Data types
print("\n=== Column dtypes ===")
print(df.dtypes)

# Unique landing pad IDs
print("\n=== Unique LandingPad values ===")
print(df["LandingPad"].unique())

# Column names
print("\n=== Columns ===")
print(df.columns)


# ---------------------------------------------------------------------------
# TASK 1: Number of launches per site
# ---------------------------------------------------------------------------
site_count = df["LaunchSite"].value_counts()
print("\n=== TASK 1 — Launches per site ===")
print(site_count)


# ---------------------------------------------------------------------------
# TASK 2: Number and occurrence of each orbit
# ---------------------------------------------------------------------------
launches_by_orbit = df["Orbit"].value_counts()
print("\n=== TASK 2 — Launches per orbit ===")
print(launches_by_orbit)

# Launch sites excluding GTO (transfer orbit, not itself geostationary)
non_gto_sites = df[df["Orbit"] != "GTO"]["LaunchSite"].value_counts()
print("\n=== Launch sites (excluding GTO) ===")
print(non_gto_sites)


# ---------------------------------------------------------------------------
# TASK 3: Mission outcome counts
# ---------------------------------------------------------------------------
landing_outcomes = df["Outcome"].value_counts()
print("\n=== TASK 3 — Landing outcomes ===")
print(landing_outcomes)

# Enumerate outcomes
print("\n=== Outcome index mapping ===")
for i, outcome in enumerate(landing_outcomes.keys()):
    print(i, outcome)


# ---------------------------------------------------------------------------
# TASK 4: Create training label (Class column)
# ---------------------------------------------------------------------------

# Unsuccessful landing outcomes
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
print("\n=== Bad outcomes (Class = 0) ===")
print(bad_outcomes)

# Class: 1 = successful landing, 0 = unsuccessful
landing_class = (~df["Outcome"].isin(bad_outcomes)).astype(int)

df["Class"] = landing_class

print("\n=== First 8 rows — Class column ===")
print(df[["Class"]].head(8))

# Overall success rate
success_rate = df["Class"].mean()
print(f"\n=== Overall landing success rate: {success_rate:.4f} ===")

# Count of True ASDS successful landings
count_true_asds = ((df["Outcome"] == "True ASDS") & (df["Class"] == 1)).sum()
print(f"\n=== True ASDS successful landings: {count_true_asds} ===")

# Final column list
print("\n=== Final columns ===")
print(df.columns)


# ---------------------------------------------------------------------------
# 5. Export to CSV
# ---------------------------------------------------------------------------
OUTPUT_FILE = "dataset_part_2.csv"
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nDataset saved to '{OUTPUT_FILE}'")
