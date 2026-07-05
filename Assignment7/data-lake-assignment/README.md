# Week 7 Assignment – Delta Lake MERGE Implementation

## Overview

This assignment demonstrates incremental data processing using Delta Lake in Azure Databricks. The project covers data loading, data cleaning, Delta Table creation, incremental dataset generation, MERGE operation, and validation of results.

---

## Objectives

- Load the Superstore dataset into Apache Spark.
- Perform basic data cleaning.
- Create a Delta Table.
- Generate an incremental dataset.
- Apply the Delta Lake MERGE operation.
- Validate the final results.
- Display the updated dataset.

---

## Technologies Used

- Azure Databricks
- Apache Spark (PySpark)
- Delta Lake
- Python
- Git & GitHub

---

## Project Structure

```text
delta-lake-assignment/
│
├── data/
│   ├── Sample - Superstore.csv
│   ├── customer_master.csv
│   └── customer_incremental.csv
│
├── notebooks/
│   └── delta_merge_assignment_final.ipynb
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── merge/
│   ├── validation/
│   └── final_output/
│
├── report/
│   └── assignment_summary.md
│
└── README.md
```

---

## Steps Performed

### Step 1 – Load Dataset
- Imported the Superstore CSV dataset into Apache Spark.
- Verified the loaded data.

### Step 2 – Explore Dataset
- Displayed sample records.
- Checked row count and column count.
- Printed schema and column names.

### Step 3 – Data Cleaning
- Checked null values.
- Removed duplicate records.
- Handled missing values.

### Step 4 – Prepare Dataset
- Renamed columns to remove spaces and special characters.
- Converted numeric columns to appropriate data types.

### Step 5 – Create Delta Table
- Created a managed Delta Table named **customer_master**.

### Step 6 – Create Incremental Dataset
- Generated updated customer records.
- Generated new customer records.
- Combined both datasets into **incremental_df**.

### Step 7 – MERGE Operation
- Updated existing records.
- Inserted new customer records.
- Performed Delta Lake MERGE successfully.

### Step 8 – Validation
- Verified total record count.
- Checked duplicate Customer IDs.
- Displayed the final merged dataset.

---

## Results

- Successfully loaded the Superstore dataset.
- Created a Delta Table.
- Generated an incremental dataset.
- Applied the MERGE operation successfully.
- Validated the final dataset after MERGE.

---

## Learning Outcomes

Through this assignment, I learned:

- Delta Lake fundamentals
- Delta Table creation
- Data cleaning using PySpark
- Incremental data processing
- MERGE operations
- Data validation techniques
- Working with Azure Databricks

---


## Author

**Name:** Naman Garg

**Internship:** Celebal Technologies Internship

**Week:** 7

**Assignment:** Delta Lake MERGE Implementation