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
    Handles missing file, empty data, BOM, and dirty whitespace gracefully.
    """
    if not file_name:
        print("Error: No filename provided.")
        return None

    clean_file_name = str(file_name).strip().strip("'\"").lstrip("\ufeff")

    if not os.path.exists(clean_file_name):
        print(f"Error: File '{clean_file_name}' not found. Please make sure the file exists in the directory.")
        return None

    try:
        df = pd.read_csv(clean_file_name, skipinitialspace=True)

        if df.empty or len(df.columns) == 0:
            print(f"Error: File '{clean_file_name}' contains no records.")
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
                print(f"Error: Missing column '{req}' in {clean_file_name}.")
                return None

        # Clean string columns
        for str_col in ["CustomerID", "Name", "City"]:
            if str_col in df.columns:
                df[str_col] = df[str_col].astype(str).str.strip()

        # Convert numeric columns
        df["Purchases"] = pd.to_numeric(df["Purchases"], errors="coerce").fillna(0).astype(int)
        df["TotalSpent"] = pd.to_numeric(df["TotalSpent"], errors="coerce")
        df = df.dropna(subset=["TotalSpent"]).reset_index(drop=True)

        if df.empty:
            print(f"Error: File '{clean_file_name}' contains no valid records.")
            return None

        return df

    except Exception as e:
        print(f"Error reading file '{clean_file_name}': {e}")
        return None


def show_spending_statistics(df):
    """
    Test Case 1: Normal Input
    Displays Mean, Median, Highest spending customer and Lowest spending customer.
    """
    if df is None or df.empty:
        print("Error: No customer data available.")
        return

    mean_val = float(df["TotalSpent"].mean())
    median_val = float(df["TotalSpent"].median())

    highest_idx = df["TotalSpent"].idxmax()
    lowest_idx = df["TotalSpent"].idxmin()

    highest_customer = df.loc[highest_idx]
    lowest_customer = df.loc[lowest_idx]

    print(f"Mean spend: Rs. {mean_val:.2f}")
    print(f"Median spend: Rs. {median_val:.2f}")
    print(f"Highest: {highest_customer['Name']} (Rs. {format_amount(highest_customer['TotalSpent'])})")
    print(f"Lowest: {lowest_customer['Name']} (Rs. {format_amount(lowest_customer['TotalSpent'])})")


def show_high_value_customers(df, limit_input=None):
    """
    Test Case 2 & 3:
    Prompts user for spending limit, validates input, and filters customers.
    """
    if df is None or df.empty:
        print("Error: No customer data available.")
        return

    if limit_input is None:
        try:
            limit_input = input("Enter spending limit: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            return
    else:
        limit_input = str(limit_input).strip()

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


def run_self_tests() -> int:
    """Executes the automated acceptance test suite verifying all test scenarios."""
    import unittest
    import io
    from contextlib import redirect_stdout

    class TestRetailCustomerAnalyzer(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            cls.csv_benchmark = os.path.join(base_dir, "customers.csv")
            cls.csv_empty = os.path.join(base_dir, "test_case_empty.csv")
            cls.csv_boundary = os.path.join(base_dir, "test_case2_boundary.csv")
            cls.csv_edge = os.path.join(base_dir, "test_case3_edge_cases.csv")
            cls.csv_dirty = os.path.join(base_dir, "test_case4_dirty.csv")

        def test_case_1_normal_input_statistics(self):
            df = load_customer_data(self.csv_benchmark)
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 8)
            self.assertAlmostEqual(df["TotalSpent"].mean(), 9125.0, places=2)
            self.assertAlmostEqual(df["TotalSpent"].median(), 7500.0, places=2)
            highest = df.loc[df["TotalSpent"].idxmax()]
            lowest = df.loc[df["TotalSpent"].idxmin()]
            self.assertEqual(highest["Name"], "Chitra")
            self.assertEqual(highest["TotalSpent"], 25000)
            self.assertEqual(lowest["Name"], "Deepak")
            self.assertEqual(lowest["TotalSpent"], 800)

        def test_case_2_boundary_minimum_input(self):
            df = load_customer_data(self.csv_benchmark)
            captured = io.StringIO()
            with redirect_stdout(captured):
                show_high_value_customers(df, limit_input="25000")
            out = captured.getvalue().strip()
            self.assertIn("C03 | Chitra | Raipur | Rs. 25000", out)

        def test_case_3a_invalid_non_numeric_input(self):
            df = load_customer_data(self.csv_benchmark)
            captured = io.StringIO()
            with redirect_stdout(captured):
                show_high_value_customers(df, limit_input="abc")
            self.assertEqual(captured.getvalue().strip(), "Invalid amount. Please enter a number.")

        def test_case_3b_invalid_negative_input(self):
            df = load_customer_data(self.csv_benchmark)
            captured = io.StringIO()
            with redirect_stdout(captured):
                show_high_value_customers(df, limit_input="-500")
            self.assertEqual(captured.getvalue().strip(), "Amount must be 0 or more.")

        def test_case_4_city_wise_summary(self):
            df = load_customer_data(self.csv_benchmark)
            captured = io.StringIO()
            with redirect_stdout(captured):
                show_city_wise_summary(df)
            lines = captured.getvalue().strip().split("\n")
            self.assertEqual(len(lines), 3)
            self.assertIn("Raipur : Total Rs. 43000 | Average Rs. 14333.33", lines[0])
            self.assertIn("Bhilai : Total Rs. 15800 | Average Rs. 7900.00", lines[1])
            self.assertIn("Durg : Total Rs. 14200 | Average Rs. 4733.33", lines[2])

        def test_case_empty_dataset_handling(self):
            df = load_customer_data(self.csv_empty)
            self.assertIsNone(df)

        def test_case_dirty_headers_and_whitespace(self):
            df = load_customer_data(self.csv_dirty)
            self.assertIsNotNone(df)
            self.assertEqual(len(df), 5)
            highest = df.loc[df["TotalSpent"].idxmax()]
            self.assertEqual(highest["Name"], "Amit Patel")

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRetailCustomerAnalyzer)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    return 0 if res.wasSuccessful() else 1


def main():
    """
    Runs the program from the console with an interactive menu.
    Supports optional CSV file path argument: python main.py <custom_dataset.csv>
    """
    csv_file = "customers.csv"

    # Support command-line argument for test CSV datasets
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        csv_file = sys.argv[1]
    elif len(sys.argv) > 2 and sys.argv[1] in ["--file", "-f"]:
        csv_file = sys.argv[2]

    # Handle missing file or prompt for path
    if not os.path.exists(csv_file):
        print(f"Warning: File '{csv_file}' was not found in the current directory.")
        try:
            user_file = input("Enter the path/name of your CSV file: ").strip()
            if user_file:
                csv_file = user_file
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            sys.exit(0)

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

        try:
            choice = input("Enter your choice (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program. Thank you!")
            break

        # Support both option numbers and option names
        choice_clean = choice.lower().replace("-", " ").strip()

        if (
            choice_clean in ["1", "spending statistics", "spending"]
            or choice_clean.startswith("1.")
            or choice_clean.startswith("1 ")
            or choice_clean == "1"
        ):
            print()
            show_spending_statistics(df)
        elif (
            choice_clean in ["2", "high value customers", "high value"]
            or choice_clean.startswith("2.")
            or choice_clean.startswith("2 ")
            or choice_clean == "2"
        ):
            print()
            show_high_value_customers(df)
        elif (
            choice_clean in ["3", "city wise summary", "city summary"]
            or choice_clean.startswith("3.")
            or choice_clean.startswith("3 ")
            or choice_clean == "3"
        ):
            print()
            show_city_wise_summary(df)
        elif (
            choice_clean in ["4", "exit", "quit", "q", "close"]
            or choice_clean.startswith("4.")
            or choice_clean.startswith("4 ")
            or choice_clean == "4"
        ):
            print("\nExiting program. Thank you!")
            break
        else:
            print("Invalid choice! Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--test", "-t", "test"]:
        sys.exit(run_self_tests())
    else:
        main()
