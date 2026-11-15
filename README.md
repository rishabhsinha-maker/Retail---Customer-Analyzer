# Retail Customer Analyzer (PS No. 74)

[![Python 3](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x%20%7C%203.x-150458.svg)](https://pandas.pydata.org/)

> **Rungta International Skills University**  
> **School of Computer Science and Engineering**  
> *Bachelor of Technology - Computer Science and Engineering (Artificial Intelligence and Machine Learning in association with Microsoft)*

A standalone, console-based Python 3 retail customer analytics project developed under **Problem Statement No. 74**. The program loads customer transaction records from `customers.csv` using **Pandas**, calculates statistical measures, filters high-value accounts based on user input, and outputs city-wise aggregated spending.

---

## 📌 Problem Statement Details

- **PS No.:** 74
- **Project Title:** Retail Customer Analyzer
- **Description:** Read `customers.csv` with Pandas. Show mean, median, highest and lowest spending, list customers who spent at least a limit entered by the user, and show city-wise total and average spending.
- **Language:** Python 3
- **Concepts:** Pandas, Filtering, Grouping, Statistics

---

## 🚀 Bare Minimum Requirements Compliance

| # | Bare Minimum Requirement | Implementation Detail | Status |
|---|--------------------------|-----------------------|:------:|
| **1** | Write the solution in Python 3 (one `.py` file) and run it from the console | Standalone code implemented in [`retail_customer_analyzer.py`](retail_customer_analyzer.py) and executed via console | **PASS** |
| **2** | Load `customers.csv` with Pandas and handle a missing file | Validated in `load_customer_data()` catching missing files and notifying the user without crashing | **PASS** |
| **3** | Calculate mean, median, highest and lowest `TotalSpent` | Calculated in `show_spending_statistics()` using Pandas `.mean()`, `.median()`, `.idxmax()`, and `.idxmin()` | **PASS** |
| **4** | Filter and list customers whose `TotalSpent` is at least the limit entered by the user | Implemented in `show_high_value_customers()` with user input and validation | **PASS** |
| **5** | Test the program with all four test cases | Tested and verified manually through console interactive inputs | **PASS** |

---

## 📂 Project Structure

```text
Retail Customer Analyzer/
│
├── retail_customer_analyzer.py      # Standalone single-file solution (Requirement 1)
├── main.py                          # Application launcher
├── customers.csv                    # Primary customer dataset (8 records)
├── summary.md                       # Comprehensive summary and test report
├── problem_statement.jpeg           # Official problem statement reference
├── test_case_1_terminal.png         # Terminal screenshot for Test Case 1
├── test_case_2_terminal.png         # Terminal screenshot for Test Case 2
├── test_case_3_terminal.png         # Terminal screenshot for Test Case 3
├── test_case_4_terminal.png         # Terminal screenshot for Test Case 4
├── terminal_all_testcases.png       # Complete terminal session screenshot
├── requirements.txt                 # Project dependencies (pandas, numpy, matplotlib)
├── .gitignore                       # Git ignore file
└── README.md                        # Project documentation
```

---

## 📊 Sample Data (`customers.csv`)

```csv
CustomerID,Name,City,Purchases,TotalSpent
C01,Asha,Raipur,5,12000
C02,Bhavin,Durg,2,3000
C03,Chitra,Raipur,8,25000
C04,Deepak,Bhilai,1,800
C05,Esha,Durg,4,9000
C06,Farhan,Raipur,3,6000
C07,Gita,Bhilai,6,15000
C08,Hari,Durg,2,2200
```

---

## 🧪 Test Cases & Expected Console Outputs

### Test Case 1: Normal Input (Spending statistics)
- **Menu Choice:** `1` (or `Spending statistics`)
- **Console Output:**
```text
Mean spend: Rs. 9125.00
Median spend: Rs. 7500.00
Highest: Chitra (Rs. 25000)
Lowest: Deepak (Rs. 800)
```

---

### Test Case 2: Boundary / Minimum Input (High-value customers)
- **Menu Choice:** `2` (or `High-value customers`)
- **User Input (Limit):** `25000`
- **Console Output:**
```text
High-value customers (TotalSpent >= 25000):
C03 | Chitra | Raipur | Rs. 25000
```

---

### Test Case 3: Invalid Input
- **(a) Non-numeric input:**
  - **Menu Choice:** `2`
  - **User Input (Limit):** `abc`
  - **Console Output:**
  ```text
  Invalid amount. Please enter a number.
  ```
- **(b) Negative amount:**
  - **Menu Choice:** `2`
  - **User Input (Limit):** `-500`
  - **Console Output:**
  ```text
  Amount must be 0 or more.
  ```

---

### Test Case 4: Different Valid Scenario (City-wise summary)
- **Menu Choice:** `3` (or `City-wise summary`)
- **Console Output:**
```text
Raipur : Total Rs. 43000 | Average Rs. 14333.33
Bhilai : Total Rs. 15800 | Average Rs. 7900.00
Durg : Total Rs. 14200 | Average Rs. 4733.33
```

---

## 💻 How to Run the Program

1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```bash
   cd "Retail---Customer-Analyzer"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Python file:
   ```bash
   python retail_customer_analyzer.py
   ```
   *(or run `python main.py`)*
5. Select options `1`, `2`, `3`, or `4` from the interactive console menu.

See [summary.md](summary.md) for full test case verification and screenshots.
