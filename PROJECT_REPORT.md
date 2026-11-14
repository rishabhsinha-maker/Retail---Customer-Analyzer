# Academic Project Report: Retail Customer Analyzer

**Course:** Bachelor of Technology - Computer Science and Engineering  
**Specialization:** Artificial Intelligence and Machine Learning in association with Microsoft  
**School:** School of Computer Science and Engineering  
**Institution:** Rungta International Skills University  
**Subject:** Python Programming & Data Analytics Lab  
**Problem Statement No.:** 74  
**Project Title:** Retail Customer Analyzer  

---

## 1. Abstract
The **Retail Customer Analyzer** is a console application developed using **Python 3** and **Pandas** to fulfill **Problem Statement No. 74**. The program loads customer purchase records from a CSV file, performs statistical calculations (mean, median, highest, lowest spending), filters customers based on a minimum spending threshold entered interactively by the user, and computes aggregated total and average spending by city. Robust error handling is included to manage missing files and invalid user inputs.

---

## 2. Problem Statement & Objectives

### 2.1 Problem Definition
Retail businesses need quick insights into customer purchasing behaviors across various cities. This project implements a single-file Python script to:
1. Ingest `customers.csv` using Pandas while safely handling missing files.
2. Calculate and display core spending statistics: Mean, Median, Highest, and Lowest spenders.
3. Allow users to input a spending limit and display all customers meeting or exceeding that threshold.
4. Generate a city-wise spending summary showing total expenditure and average spending per city.
5. Provide a clear interactive console menu.

---

## 3. Dataset Description

The application processes records with the following columns:
- `CustomerID`: Unique customer code (e.g., C01, C02)
- `Name`: Customer Name
- `City`: Residential/Purchasing City (e.g., Raipur, Durg, Bhilai)
- `Purchases`: Number of purchases made
- `TotalSpent`: Total monetary expenditure in Rupees (Rs.)

### Sample Dataset (`customers.csv`):
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

## 4. Implementation Details

The solution is contained in a single Python script ([`retail_customer_analyzer.py`](retail_customer_analyzer.py)) structured into clean functions:

1. **`load_customer_data(file_name)`**:
   - Uses `os.path.exists()` to check if the file exists.
   - Loads the file into a Pandas DataFrame using `pd.read_csv()`.
   - Normalizes column names and validates required headers.
   - Converts `TotalSpent` and `Purchases` to numeric types.

2. **`show_spending_statistics(df)`**:
   - Evaluates `df['TotalSpent'].mean()` and `df['TotalSpent'].median()`.
   - Finds highest and lowest spenders using `.idxmax()` and `.idxmin()`.

3. **`show_high_value_customers(df)`**:
   - Prompts user for a threshold amount.
   - Catches non-numeric inputs with `"Invalid amount. Please enter a number."`.
   - Catches negative values with `"Amount must be 0 or more."`.
   - Filters records using `df[df['TotalSpent'] >= limit_val]`.

4. **`show_city_wise_summary(df)`**:
   - Groups data using `.groupby('City')`.
   - Calculates Total (`sum`) and Average (`mean`).
   - Sorts descending by Total spending.

5. **`main()`**:
   - Displays a clean console menu (1 to 4) and processes user input in a loop.

---

## 5. Test Cases & Results

### 5.1 Test Case 1: Normal Input (Spending statistics)
- **Menu Choice:** `1`
- **Output:**
```text
Mean spend: Rs. 9125.00
Median spend: Rs. 7500.00
Highest: Chitra (Rs. 25000)
Lowest: Deepak (Rs. 800)
```
- **Result:** PASS (Matches calculation: Sum = 73000 / 8 = 9125.00; Median = 7500.00).

### 5.2 Test Case 2: Boundary / Minimum Input (High-value customers)
- **Menu Choice:** `2`
- **Limit:** `25000`
- **Output:**
```text
High-value customers (TotalSpent >= 25000):
C03 | Chitra | Raipur | Rs. 25000
```
- **Result:** PASS (Accurately filters only customer C03).

### 5.3 Test Case 3: Invalid Input
- **Scenario (a):** Limit = `abc`
  - **Output:** `Invalid amount. Please enter a number.`
  - **Result:** PASS
- **Scenario (b):** Limit = `-500`
  - **Output:** `Amount must be 0 or more.`
  - **Result:** PASS

### 5.4 Test Case 4: Different Valid Scenario (City-wise summary)
- **Menu Choice:** `3`
- **Output:**
```text
Raipur : Total Rs. 43000 | Average Rs. 14333.33
Bhilai : Total Rs. 15800 | Average Rs. 7900.00
Durg : Total Rs. 14200 | Average Rs. 4733.33
```
- **Result:** PASS (Accurately grouped and sorted by total expenditure).

---

## 6. Conclusion
The **Retail Customer Analyzer (PS 74)** successfully satisfies all problem requirements, adheres strictly to single-file Python 3 constraints, and passes all required test cases cleanly from the console.
