"""
Experiment 12: Exploratory Data Analysis (EDA)
Descriptive statistics, visualization, handling missing data and outliers
on a customer churn dataset.

Note: If you have a real churn CSV (e.g. 'churn.csv'), place it in the same
folder and it will be used automatically. Otherwise a sample dataset is generated.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

CSV_FILE = "churn.csv"


def load_data():
    if os.path.exists(CSV_FILE):
        print(f"Loaded dataset from '{CSV_FILE}'.")
        return pd.read_csv(CSV_FILE)

    print("'churn.csv' not found. Generating a sample customer churn dataset.")
    rng = np.random.default_rng(42)
    n = 200
    df = pd.DataFrame({
        "CustomerID": range(1, n + 1),
        "Age": rng.integers(18, 70, n).astype(float),
        "Tenure": rng.integers(1, 72, n).astype(float),
        "MonthlyCharges": rng.normal(65, 20, n).round(2),
        "Churn": rng.choice(["Yes", "No"], n, p=[0.27, 0.73]),
    })
    df["TotalCharges"] = (df["Tenure"] * df["MonthlyCharges"]).round(2)
    # Inject missing values and outliers
    df.loc[rng.choice(n, 10, replace=False), "Age"] = np.nan
    df.loc[rng.choice(n, 8, replace=False), "MonthlyCharges"] = np.nan
    df.loc[[5, 50, 120], "MonthlyCharges"] = [400, 450, 500]
    return df


def numeric_cols(df):
    return df.select_dtypes(include=np.number).drop(columns=["CustomerID"], errors="ignore")


def overview(df):
    print("Shape:", df.shape)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)


def descriptive_stats(df):
    num = numeric_cols(df)
    print("Summary (describe):")
    print(num.describe())
    print("\nMean:")
    print(num.mean().round(2))
    print("\nMedian:")
    print(num.median().round(2))
    print("\nMode:")
    print(num.mode().iloc[0])
    print("\nStandard Deviation:")
    print(num.std().round(2))
    print("\nVariance:")
    print(num.var().round(2))
    print("\nQuantiles (25%, 50%, 75%):")
    print(num.quantile([0.25, 0.5, 0.75]))
    print("\nChurn counts:")
    print(df["Churn"].value_counts())


def missing_data(df):
    print("Missing values per column:")
    print(df.isnull().sum())
    #Om Kutwal Sy-12 Roll no. 70
    df_dropped = df.dropna()
    print(f"\nRows after dropna(): {len(df_dropped)} (originally {len(df)})")
    df_filled = df.copy()
    for col in numeric_cols(df).columns:
        df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
    print("\nMissing values after filling with mean:")
    print(df_filled.isnull().sum())
    return df_filled


def detect_outliers(df):
    num = numeric_cols(df).fillna(numeric_cols(df).mean())
    z = num.apply(zscore)
    print("Outliers detected using Z-score (|z| > 3):")
    for col in num.columns:
        count = int((z[col].abs() > 3).sum())
        print(f"{col:<16}: {count}")
    print("\nOutliers detected using IQR method:")
    for col in num.columns:
        q1, q3 = num[col].quantile(0.25), num[col].quantile(0.75)
        iqr = q3 - q1
        count = int(((num[col] < q1 - 1.5 * iqr) | (num[col] > q3 + 1.5 * iqr)).sum())
        print(f"{col:<16}: {count}")


def handle_outliers(df):
    clean = df.copy()
    for col in numeric_cols(df).columns:
        clean[col] = clean[col].fillna(clean[col].mean())
    col = "MonthlyCharges"
    z = zscore(clean[col])
    removed = clean[np.abs(z) <= 3]
    print(f"Rows before removing outliers: {len(clean)}")
    print(f"Rows after removing outliers : {len(removed)}")
    upper = clean[col].mean() + 3 * clean[col].std()
    lower = clean[col].mean() - 3 * clean[col].std()
    capped = clean[col].clip(lower=lower, upper=upper)
    print(f"\n{col} max before capping: {clean[col].max()}")
    print(f"{col} max after capping : {round(capped.max(), 2)}")


def visualize(df):
    clean = df.copy()
    for col in numeric_cols(df).columns:
        clean[col] = clean[col].fillna(clean[col].mean())

    plt.hist(clean["Age"], bins=10, edgecolor="black")
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.show()

    sns.boxplot(y=clean["MonthlyCharges"])
    plt.title("Box Plot of Monthly Charges")
    plt.show()

    plt.scatter(clean["Tenure"], clean["TotalCharges"])
    plt.title("Tenure vs Total Charges")
    plt.xlabel("Tenure")
    plt.ylabel("Total Charges")
    plt.show()

    sns.heatmap(numeric_cols(clean).corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()

    sns.countplot(x="Churn", data=clean)
    plt.title("Customer Churn Count")
    plt.show()


def print_menu():
    print("\n===== EDA - CUSTOMER CHURN DATASET =====")
    print("1. Dataset overview")
    print("2. Descriptive statistics")
    print("3. Handle missing data")
    print("4. Detect outliers")
    print("5. Handle outliers (remove / cap)")
    print("6. Visualizations (plots)")
    print("7. Exit")
    print("=========================================")


def main():
    df = load_data()
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            overview(df)
        elif choice == "2":
            descriptive_stats(df)
        elif choice == "3":
            df = missing_data(df)
        elif choice == "4":
            detect_outliers(df)
        elif choice == "5":
            handle_outliers(df)
        elif choice == "6":
            visualize(df)
        elif choice == "7":
            print("Exiting the EDA Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
