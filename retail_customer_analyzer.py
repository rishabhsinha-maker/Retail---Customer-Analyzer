"""
Retail Customer Analyzer
========================
Institution : Rungta International Skills University
School      : School of Computer Science and Engineering
Program     : Bachelor of Technology - Computer Science and Engineering
              (Artificial Intelligence and Machine Learning in association with Microsoft)
PS No.      : 74
Title       : Retail Customer Analyzer
Language    : Python 3
Concepts    : Pandas, Filtering, Grouping, Statistics
"""

import os
import sys
import pandas as pd


def format_amount(value):
    """
    Format monetary amounts:
    Display as an integer if whole number (e.g., 25000), otherwise with 2 decimal places.
    """
    try:
        val_float = float(value)
        if val_float.is_integer():
            return str(int(val_float))
        return f"{val_float:.2f}"
    except (ValueError, TypeError):
        return str(value)


def load_customer_data(file_name="customers.csv"):
    """
    Load customer transaction data from CSV using Pandas.
    Handles missing file and empty data gracefully.
    """
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found. Please make sure the file exists in the directory.")
        return None

    try:
        df = pd.read_csv(file_name)

        if df.empty:
            print(f"Error: File '{file_name}' contains no records.")
            return None

        # Standardize column headers
        col_map = {}
        for col in df.columns:
            cleaned = str(col).strip().lstrip("\ufeff")
            lower = cleaned.lower()
            if "customerid" in lower or "id" == lower:
                col_map[col] = "CustomerID"
            elif "name" in lower:
                col_map[col] = "Name"
            elif "city" in lower:
                col_map[col] = "City"
            elif "purchases" in lower:
                col_map[col] = "Purchases"
            elif "totalspent" in lower or "spent" in lower:
                col_map[col] = "TotalSpent"

        df = df.rename(columns=col_map)

        # Validate required columns
        required = ["CustomerID", "Name", "City", "Purchases", "TotalSpent"]
        for req in required:
            if req not in df.columns:
                print(f"Error: Missing column '{req}' in {file_name}.")
                return None

        # Convert numeric columns
        df["Purchases"] = pd.to_numeric(df["Purchases"], errors="coerce").fillna(0).astype(int)
        df["TotalSpent"] = pd.to_numeric(df["TotalSpent"], errors="coerce")
        df = df.dropna(subset=["TotalSpent"]).reset_index(drop=True)

        return df

    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        return None


def show_spending_statistics(df):
    """
    Test Case 1: Normal Input
    Displays Mean, Median, Highest spending customer and Lowest spending customer.
    """
    if df is None or df.empty:
        print("Error: No customer data available.")
        return

    mean_val = df["TotalSpent"].mean()
    median_val = df["TotalSpent"].median()

    highest_idx = df["TotalSpent"].idxmax()
    lowest_idx = df["TotalSpent"].idxmin()

    highest_customer = df.loc[highest_idx]
    lowest_customer = df.loc[lowest_idx]

    print(f"Mean spend: Rs. {mean_val:.2f}")
    print(f"Median spend: Rs. {median_val:.2f}")
    print(f"Highest: {highest_customer['Name']} (Rs. {format_amount(highest_customer['TotalSpent'])})")
    print(f"Lowest: {lowest_customer['Name']} (Rs. {format_amount(lowest_customer['TotalSpent'])})")


def show_high_value_customers(df):
    """
    Test Case 2 & 3:
    Prompts user for spending limit, validates input, and filters customers.
    """
    if df is None or df.empty:
        print("Error: No customer data available.")
        return

    limit_input = input("Enter spending limit: ").strip()

    # Test Case 3a: Validate numeric input
    try:
        limit_val = float(limit_input)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Test Case 3b: Validate non-negative value
    if limit_val < 0:
        print("Amount must be 0 or more.")
        return

    formatted_limit = format_amount(limit_val)
    filtered_df = df[df["TotalSpent"] >= limit_val]

    print(f"High-value customers (TotalSpent >= {formatted_limit}):")
    if filtered_df.empty:
        print(f"No customers found with TotalSpent >= {formatted_limit}.")
        return

    for _, row in filtered_df.iterrows():
        cid = str(row["CustomerID"]).strip()
        name = str(row["Name"]).strip()
        city = str(row["City"]).strip()
        spent = format_amount(row["TotalSpent"])
        print(f"{cid} | {name} | {city} | Rs. {spent}")


def show_city_wise_summary(df):
    """
    Test Case 4:
    Groups by City, displays Total and Average spending per city, sorted descending by Total.
    """
    if df is None or df.empty:
        print("Error: No customer data available.")
        return

    city_summary = df.groupby("City", as_index=False).agg(
        Total=("TotalSpent", "sum"),
        Average=("TotalSpent", "mean")
    ).sort_values(by="Total", ascending=False).reset_index(drop=True)

    for _, row in city_summary.iterrows():
        city_name = str(row["City"]).strip()
        total_str = format_amount(row["Total"])
        avg_float = float(row["Average"])
        print(f"{city_name} : Total Rs. {total_str} | Average Rs. {avg_float:.2f}")


def main():
    """
    Runs the program from the console with an interactive menu.
    """
    csv_file = "customers.csv"

    # Handle missing file or prompt for path
    if not os.path.exists(csv_file):
        print(f"Warning: Default '{csv_file}' was not found in the current directory.")
        user_file = input("Enter the path/name of your CSV file: ").strip()
        if user_file:
            csv_file = user_file

    df = load_customer_data(csv_file)
    if df is None:
        print("Exiting program.")
        sys.exit(1)

    while True:
        print("\n" + "=" * 40)
        print("       RETAIL CUSTOMER ANALYZER")
        print("=" * 40)
        print("1. Spending statistics")
        print("2. High-value customers")
        print("3. City-wise summary")
        print("4. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-4): ").strip()

        # Support both option numbers and option names
        choice_clean = choice.lower().replace("-", " ")

        if choice_clean in ["1", "spending statistics", "spending"]:
            print()
            show_spending_statistics(df)
        elif choice_clean in ["2", "high value customers", "high value"]:
            print()
            show_high_value_customers(df)
        elif choice_clean in ["3", "city wise summary", "city summary"]:
            print()
            show_city_wise_summary(df)
        elif choice_clean in ["4", "exit", "quit", "q"]:
            print("\nExiting program. Thank you!")
            break
        else:
            print("Invalid choice! Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
