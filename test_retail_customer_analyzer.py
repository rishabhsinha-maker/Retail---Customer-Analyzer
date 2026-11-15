"""
Test Suite for Retail Customer Analyzer (PS No. 74)
===================================================
Institution : Rungta International Skills University
School      : School of Computer Science and Engineering
PS No.      : 74
Title       : Retail Customer Analyzer
Language    : Python 3
Framework   : Pytest / Unittest
"""

import io
import os
import sys
import tempfile
import pytest
import pandas as pd
from contextlib import redirect_stdout
from unittest.mock import patch

# Ensure the current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retail_customer_analyzer import (
    format_amount,
    load_customer_data,
    show_spending_statistics,
    show_high_value_customers,
    show_city_wise_summary,
    main,
)


@pytest.fixture
def sample_csv_path():
    """Returns absolute path to the standard customers.csv."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "customers.csv")
    assert os.path.exists(path), f"customers.csv not found at {path}"
    return path


@pytest.fixture
def loaded_dataframe(sample_csv_path):
    """Returns the loaded and validated customer DataFrame."""
    df = load_customer_data(sample_csv_path)
    assert df is not None
    assert len(df) == 8
    return df


# ============================================================================
# 1. Format Amount Unit Tests
# ============================================================================
class TestAmountFormatting:
    """Tests for the format_amount utility function."""

    def test_format_amount_whole_number(self):
        assert format_amount(25000) == "25000"
        assert format_amount("25000") == "25000"

    def test_format_amount_float_as_integer(self):
        assert format_amount(25000.0) == "25000"
        assert format_amount(800.00) == "800"

    def test_format_amount_two_decimal_places(self):
        assert format_amount(14333.33333) == "14333.33"
        assert format_amount(9125.5) == "9125.50"
        assert format_amount("123.456") == "123.46"

    def test_format_amount_invalid_type_fallback(self):
        assert format_amount("invalid_amount") == "invalid_amount"
        assert format_amount(None) == "None"


# ============================================================================
# 2. Data Loading & CSV Handling Tests
# ============================================================================
class TestCustomerDataLoader:
    """Tests for load_customer_data handling valid files, missing files, and malformed CSVs."""

    def test_load_existing_default_file(self, sample_csv_path):
        df = load_customer_data(sample_csv_path)
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 8
        required_cols = ["CustomerID", "Name", "City", "Purchases", "TotalSpent"]
        for col in required_cols:
            assert col in df.columns

    def test_load_missing_file(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = load_customer_data("non_existent_customers_file_9999.csv")
        captured = output.getvalue()
        assert result is None
        assert "Error: File 'non_existent_customers_file_9999.csv' not found" in captured

    def test_load_empty_csv(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            temp_path = f.name

        try:
            output = io.StringIO()
            with redirect_stdout(output):
                result = load_customer_data(temp_path)
            captured = output.getvalue()
            assert result is None
            assert "contains no records" in captured or "Error reading file" in captured
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_csv_missing_required_column(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("CustomerID,Name,City,Purchases\nC01,Asha,Raipur,5\n")
            temp_path = f.name

        try:
            output = io.StringIO()
            with redirect_stdout(output):
                result = load_customer_data(temp_path)
            captured = output.getvalue()
            assert result is None
            assert "Missing column 'TotalSpent'" in captured
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_csv_with_header_variations_and_bom(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8-sig") as f:
            f.write("id, customer_name, customer_city, num_purchases, spent\n")
            f.write("C99,TestUser,Raipur,10,5000\n")
            temp_path = f.name

        try:
            df = load_customer_data(temp_path)
            assert df is not None
            assert len(df) == 1
            assert df.iloc[0]["CustomerID"] == "C99"
            assert df.iloc[0]["TotalSpent"] == 5000
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


# ============================================================================
# 3. Test Case 1: Normal Input (Spending Statistics)
# ============================================================================
class TestCase1SpendingStatistics:
    """
    Test Case 1: Normal Input (Spending statistics)
    - Mean spend: Rs. 9125.00
    - Median spend: Rs. 7500.00
    - Highest: Chitra (Rs. 25000)
    - Lowest: Deepak (Rs. 800)
    """

    def test_spending_statistics_output(self, loaded_dataframe):
        output = io.StringIO()
        with redirect_stdout(output):
            show_spending_statistics(loaded_dataframe)
        captured = output.getvalue()

        assert "Mean spend: Rs. 9125.00" in captured
        assert "Median spend: Rs. 7500.00" in captured
        assert "Highest: Chitra (Rs. 25000)" in captured
        assert "Lowest: Deepak (Rs. 800)" in captured

    def test_spending_statistics_empty_dataframe(self):
        output = io.StringIO()
        empty_df = pd.DataFrame()
        with redirect_stdout(output):
            show_spending_statistics(empty_df)
        captured = output.getvalue()
        assert "Error: No customer data available." in captured


# ============================================================================
# 4. Test Case 2: Boundary / Minimum Input (High-value customers)
# ============================================================================
class TestCase2HighValueCustomers:
    """
    Test Case 2: Boundary / Minimum Input
    - Limit: 25000
    - Output:
        High-value customers (TotalSpent >= 25000):
        C03 | Chitra | Raipur | Rs. 25000
    """

    def test_high_value_customers_boundary_25000(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="25000"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()

        assert "High-value customers (TotalSpent >= 25000):" in captured
        assert "C03 | Chitra | Raipur | Rs. 25000" in captured
        # Ensure lower spenders are not included
        assert "Deepak" not in captured
        assert "Hari" not in captured

    def test_high_value_customers_intermediate_limit_10000(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="10000"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()

        assert "High-value customers (TotalSpent >= 10000):" in captured
        assert "C01 | Asha | Raipur | Rs. 12000" in captured
        assert "C03 | Chitra | Raipur | Rs. 25000" in captured
        assert "C07 | Gita | Bhilai | Rs. 15000" in captured
        assert "Deepak" not in captured

    def test_high_value_customers_zero_limit(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="0"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()

        assert "High-value customers (TotalSpent >= 0):" in captured
        for cid in ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08"]:
            assert cid in captured

    def test_high_value_customers_exceeding_max_limit(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="50000"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()

        assert "No customers found with TotalSpent >= 50000." in captured

    def test_high_value_customers_empty_dataframe(self):
        output = io.StringIO()
        empty_df = pd.DataFrame()
        with redirect_stdout(output):
            show_high_value_customers(empty_df)
        captured = output.getvalue()
        assert "Error: No customer data available." in captured


# ============================================================================
# 5. Test Case 3: Invalid Input
# ============================================================================
class TestCase3InvalidInputs:
    """
    Test Case 3: Invalid Input
    - (a) Non-numeric input: "abc" -> "Invalid amount. Please enter a number."
    - (b) Negative amount: "-500" -> "Amount must be 0 or more."
    """

    def test_case_3a_non_numeric_input_string(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="abc"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()
        assert "Invalid amount. Please enter a number." in captured

    def test_case_3a_non_numeric_special_chars(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="$%#@"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()
        assert "Invalid amount. Please enter a number." in captured

    def test_case_3b_negative_integer(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="-500"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()
        assert "Amount must be 0 or more." in captured

    def test_case_3b_negative_float(self, loaded_dataframe):
        output = io.StringIO()
        with patch("builtins.input", return_value="-0.01"):
            with redirect_stdout(output):
                show_high_value_customers(loaded_dataframe)
        captured = output.getvalue()
        assert "Amount must be 0 or more." in captured


# ============================================================================
# 6. Test Case 4: City-Wise Summary
# ============================================================================
class TestCase4CityWiseSummary:
    """
    Test Case 4: Different Valid Scenario (City-wise summary)
    - Raipur : Total Rs. 43000 | Average Rs. 14333.33
    - Bhilai : Total Rs. 15800 | Average Rs. 7900.00
    - Durg : Total Rs. 14200 | Average Rs. 4733.33
    """

    def test_city_wise_summary_output(self, loaded_dataframe):
        output = io.StringIO()
        with redirect_stdout(output):
            show_city_wise_summary(loaded_dataframe)
        captured = output.getvalue()

        assert "Raipur : Total Rs. 43000 | Average Rs. 14333.33" in captured
        assert "Bhilai : Total Rs. 15800 | Average Rs. 7900.00" in captured
        assert "Durg : Total Rs. 14200 | Average Rs. 4733.33" in captured

    def test_city_wise_summary_order(self, loaded_dataframe):
        """Verify sorting descending by Total spending."""
        output = io.StringIO()
        with redirect_stdout(output):
            show_city_wise_summary(loaded_dataframe)
        captured = output.getvalue()

        pos_raipur = captured.find("Raipur")
        pos_bhilai = captured.find("Bhilai")
        pos_durg = captured.find("Durg")

        assert pos_raipur != -1 and pos_bhilai != -1 and pos_durg != -1
        assert pos_raipur < pos_bhilai < pos_durg

    def test_city_wise_summary_empty_dataframe(self):
        output = io.StringIO()
        empty_df = pd.DataFrame()
        with redirect_stdout(output):
            show_city_wise_summary(empty_df)
        captured = output.getvalue()
        assert "Error: No customer data available." in captured


# ============================================================================
# 7. End-to-End Interactive CLI Menu Tests
# ============================================================================
class TestInteractiveCLIMenu:
    """Tests the main interactive console menu flow."""

    def test_menu_option_1_spending_stats_then_exit(self):
        inputs = ["1", "4"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()
        captured = output.getvalue()
        assert "RETAIL CUSTOMER ANALYZER" in captured
        assert "Mean spend: Rs. 9125.00" in captured
        assert "Exiting program. Thank you!" in captured

    def test_menu_option_2_high_value_then_exit(self):
        inputs = ["2", "25000", "4"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()
        captured = output.getvalue()
        assert "High-value customers (TotalSpent >= 25000):" in captured
        assert "C03 | Chitra | Raipur | Rs. 25000" in captured
        assert "Exiting program. Thank you!" in captured

    def test_menu_option_3_city_summary_then_exit(self):
        inputs = ["3", "4"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()
        captured = output.getvalue()
        assert "Raipur : Total Rs. 43000 | Average Rs. 14333.33" in captured
        assert "Exiting program. Thank you!" in captured

    def test_menu_invalid_option_recovery_then_exit(self):
        inputs = ["99", "4"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()
        captured = output.getvalue()
        assert "Invalid choice! Please choose 1, 2, 3, or 4." in captured
        assert "Exiting program. Thank you!" in captured

    def test_menu_named_choice_spending_then_exit(self):
        inputs = ["spending statistics", "exit"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                main()
        captured = output.getvalue()
        assert "Mean spend: Rs. 9125.00" in captured
        assert "Exiting program. Thank you!" in captured


if __name__ == "__main__":
    pytest.main(["-v", __file__])
