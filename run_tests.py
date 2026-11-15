"""
Test Runner for Retail Customer Analyzer (PS No. 74)
====================================================
Runs the full test suite with detailed output and exits with code 0 on success.
"""

import sys
import subprocess
import os

def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)

    print("=" * 70)
    print(" RETAIL CUSTOMER ANALYZER - AUTOMATED TEST SUITE (PS NO. 74)")
    print(" Institution: Rungta International Skills University")
    print(" School of Computer Science and Engineering")
    print("=" * 70)
    print("\nExecuting pytest with verbose test case reporting...\n")

    cmd = [sys.executable, "-m", "pytest", "test_retail_customer_analyzer.py", "-v", "--tb=short"]
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 70)
        print(" [SUCCESS] ALL TEST CASES PASSED WITH 100% SUCCESS RATE!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print(" [FAILURE] SOME TEST CASES FAILED. Check log output above.")
        print("=" * 70)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
