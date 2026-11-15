"""
Retail Customer Analyzer - Entry Point
======================================
PS No.: 74
Institution: Rungta International Skills University
School: School of Computer Science and Engineering
"""

import os
import sys

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retail_customer_analyzer import main, run_self_tests

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["--test", "-t", "test"]:
        sys.exit(run_self_tests())
    else:
        main()
