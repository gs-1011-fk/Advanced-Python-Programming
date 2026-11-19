"""
Experiment 11: Data Manipulation with Pandas
Series, DataFrames, indexing, data cleaning, merging and aggregation.
"""

import numpy as np
import pandas as pd


def make_series():
    return pd.Series(np.random.randint(1, 100, size=10))


def make_employee_df():
    data = {
        "ID": [1, 2, 3, 4, 5, 6],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Bob"],
        "Department": ["HR", "IT", "HR", "IT", "Finance", "IT"],
        "Age": [24, 27, None, 32, 29, 27],
        "Salary": [50000, 60000, 52000, 58000, None, 60000],
        "City": ["Pune", "Mumbai", None, "Pune", "Delhi", "Mumbai"],
    }
    return pd.DataFrame(data)


def series_demo():
    ser = make_series()
    print("Pandas Series of ten random numbers:")
    print(ser)
    print("\nSum :", ser.sum())
    print("Mean:", ser.mean())
    print("Max :", ser.max())
    print("Min :", ser.min())
    ser_custom = pd.Series(ser.values, index=list("abcdefghij"))
    print("\nSeries with custom index:")
    print(ser_custom)
    print("\nValue at label 'c':", ser_custom["c"])


def dataframe_demo(df):
    print("DataFrame:")
    print(df)
    print("\nShape:", df.shape)
    print("\nColumns:", list(df.columns))


def indexing_demo(df):
    print("Single column (Name):")
    print(df["Name"])
    print("\nMultiple columns (Name, City):")
    print(df[["Name", "City"]])
    print("\nFirst row using iloc[0]:")
    print(df.iloc[0])
    print("\nRows 1 to 3 using iloc[1:4]:")
    print(df.iloc[1:4])
    print("\nRows with label 0 to 2 using loc[0:2]:")
    print(df.loc[0:2])


def cleaning_demo(df):
    print("Missing values per column:")
    print(df.isnull().sum())
    #Om Kutwal Sy-12 Roll no. 70
    print("\nAfter dropna() (rows with missing removed):")
    print(df.dropna())
    filled = df.fillna({"Age": df["Age"].mean(), "Salary": df["Salary"].mean(), "City": "Unknown"})
    print("\nAfter fillna() (mean / 'Unknown'):")
    print(filled)
    print("\nAfter drop_duplicates() on (Name, Department):")
    print(filled.drop_duplicates(subset=["Name", "Department"]))


def merging_demo():
    df1 = pd.DataFrame({"ID": [1, 2, 3], "Name": ["Alice", "Bob", "Charlie"]})
    df2 = pd.DataFrame({"ID": [3, 4, 5], "Age": [24, 27, 22]})
    print("df1:")
    print(df1)
    print("\ndf2:")
    print(df2)
    for how in ["inner", "left", "right", "outer"]:
        print(f"\n{how.upper()} join:")
        print(pd.merge(df1, df2, on="ID", how=how))


def aggregation_demo(df):
    clean = df.drop_duplicates(subset=["Name", "Department"]).fillna(
        {"Age": df["Age"].mean(), "Salary": df["Salary"].mean()})
    grouped = clean.groupby("Department")
    print("Average salary by department:")
    print(grouped["Salary"].mean())
    print("\nSalary aggregation (mean, sum, max):")
    print(grouped["Salary"].agg(["mean", "sum", "max"]))
    print("\nOldest and youngest in each department:")
    print(grouped["Age"].agg(["max", "min"]))


def print_menu():
    print("\n===== PANDAS DATA MANIPULATION =====")
    print("1. Series with ten random numbers")
    print("2. Create and display a DataFrame")
    print("3. Indexing and selecting data")
    print("4. Data cleaning (missing values, duplicates)")
    print("5. Merging DataFrames (joins)")
    print("6. Aggregation and grouping")
    print("7. Exit")
    print("====================================")


def main():
    df = make_employee_df()
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            series_demo()
        elif choice == "2":
            dataframe_demo(df)
        elif choice == "3":
            indexing_demo(df)
        elif choice == "4":
            cleaning_demo(df)
        elif choice == "5":
            merging_demo()
        elif choice == "6":
            aggregation_demo(df)
        elif choice == "7":
            print("Exiting the Pandas Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
