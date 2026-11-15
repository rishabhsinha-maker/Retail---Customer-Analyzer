"""
Official 4 Test Cases Runner for Retail Customer Analyzer (PS No. 74)
=====================================================================
Executes the exact 4 test cases specified in the Problem Statement
and displays verified outputs and pass badges.
"""

import io
import sys
import os
from contextlib import redirect_stdout
from unittest.mock import patch

from retail_customer_analyzer import (
    load_customer_data,
    show_spending_statistics,
    show_high_value_customers,
    show_city_wise_summary,
)

def run_test_case_1(df):
    print("=" * 65)
    print("TEST CASE 1: Normal Input (Spending statistics)")
    print("=" * 65)
    out = io.StringIO()
    with redirect_stdout(out):
        show_spending_statistics(df)
    res = out.getvalue()
    print(res.strip())

    assert "Mean spend: Rs. 9125.00" in res
    assert "Median spend: Rs. 7500.00" in res
    assert "Highest: Chitra (Rs. 25000)" in res
    assert "Lowest: Deepak (Rs. 800)" in res
    print(">>> STATUS: [PASS] Test Case 1 Passed Successfully!\n")

def run_test_case_2(df):
    print("=" * 65)
    print("TEST CASE 2: Boundary / Minimum Input (High-value customers >= 25000)")
    print("=" * 65)
    print("User Input (Limit): 25000")
    out = io.StringIO()
    with patch("builtins.input", return_value="25000"):
        with redirect_stdout(out):
            show_high_value_customers(df)
    res = out.getvalue()
    print(res.strip())

    assert "High-value customers (TotalSpent >= 25000):" in res
    assert "C03 | Chitra | Raipur | Rs. 25000" in res
    assert "Deepak" not in res
    print(">>> STATUS: [PASS] Test Case 2 Passed Successfully!\n")

def run_test_case_3(df):
    print("=" * 65)
    print("TEST CASE 3: Invalid Input Validation")
    print("=" * 65)
    print("Scenario 3a: Non-numeric input ('abc')")
    out_3a = io.StringIO()
    with patch("builtins.input", return_value="abc"):
        with redirect_stdout(out_3a):
            show_high_value_customers(df)
    res_3a = out_3a.getvalue()
    print("Output:", res_3a.strip())
    assert "Invalid amount. Please enter a number." in res_3a

    print("\nScenario 3b: Negative amount input ('-500')")
    out_3b = io.StringIO()
    with patch("builtins.input", return_value="-500"):
        with redirect_stdout(out_3b):
            show_high_value_customers(df)
    res_3b = out_3b.getvalue()
    print("Output:", res_3b.strip())
    assert "Amount must be 0 or more." in res_3b

    print(">>> STATUS: [PASS] Test Case 3 Passed Successfully!\n")

def run_test_case_4(df):
    print("=" * 65)
    print("TEST CASE 4: Different Valid Scenario (City-wise summary)")
    print("=" * 65)
    out = io.StringIO()
    with redirect_stdout(out):
        show_city_wise_summary(df)
    res = out.getvalue()
    print(res.strip())

    assert "Raipur : Total Rs. 43000 | Average Rs. 14333.33" in res
    assert "Bhilai : Total Rs. 15800 | Average Rs. 7900.00" in res
    assert "Durg : Total Rs. 14200 | Average Rs. 4733.33" in res
    print(">>> STATUS: [PASS] Test Case 4 Passed Successfully!\n")

def main():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "customers.csv")
    df = load_customer_data(csv_path)
    if df is None:
        print("Error: Could not load customer dataset.")
        sys.exit(1)

    print("\n" + "#" * 65)
    print(" RETAIL CUSTOMER ANALYZER - PROBLEM STATEMENT NO. 74")
    print(" RUNNING 4 OFFICIAL TEST CASES")
    print("#" * 65 + "\n")

    run_test_case_1(df)
    run_test_case_2(df)
    run_test_case_3(df)
    run_test_case_4(df)

    print("#" * 65)
    print(" ALL 4 OFFICIAL TEST CASES VERIFIED AND PASSED (100%)")
    print("#" * 65 + "\n")

if __name__ == "__main__":
    main()
