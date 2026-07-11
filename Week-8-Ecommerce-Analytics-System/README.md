# 🛒 E-Commerce Order Analytics System

## 📌 Project Overview

The **E-Commerce Order Analytics System** is an end-to-end data analytics project developed using **Python, Pandas, SQLite, and SQL**. The project simulates an e-commerce platform by generating realistic datasets, cleaning and validating data, loading it into a relational database, performing advanced SQL analytics, and generating business reports through a command-line interface.

This project was developed as the **Week 8 Mini Project** during the internship.

---

# 🎯 Objectives

- Generate realistic e-commerce datasets
- Introduce intentional data inconsistencies
- Clean and validate data using Pandas
- Maintain referential integrity
- Load cleaned data into SQLite
- Perform SQL analytics
- Build a CLI reporting tool
- Handle edge cases

---

# 🛠️ Technologies Used

- Python 3.x
- Pandas
- SQLite
- SQL
- Faker
- Tabulate
- VS Code

---

# 📂 Project Structure

```text
Week-8-Ecommerce-Analytics-System/

│── data/
│   ├── raw/
│   └── cleaned/
│
│── database/
│   └── ecommerce.db
│
│── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   └── report_cli.py
│
│── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
│── tests/
│   └── test_edge_cases.py
│
│── output/
│   └── sample_reports/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🚀 Project Workflow

```
Generate Data
        ↓
Clean Data
        ↓
Validate Data
        ↓
Load into SQLite
        ↓
Run SQL Analytics
        ↓
Generate CLI Reports
        ↓
Perform Edge Case Testing
```

---

# 📊 Dataset

The project generates four datasets.

- customers.csv
- products.csv
- orders.csv
- order_items.csv

Each dataset contains realistic fake data.

Intentional inconsistencies include:

- Missing customer IDs
- Invalid email addresses
- Mixed date formats
- Extra spaces in product names
- Negative quantities

---

# 🧹 Data Cleaning

Implemented using Pandas.

Functions:

- clean_orders()
- clean_products()
- validate_emails()
- check_referential_integrity()

Outputs:

- customers_clean.csv
- products_clean.csv
- orders_clean.csv
- order_items_clean.csv

---

# 🗄 Database

SQLite database:

```
database/ecommerce.db
```

Tables:

- Customers
- Products
- Orders
- Order Items

Primary Keys and Foreign Keys are implemented.

---

# 📈 SQL Analytics

Implemented SQL concepts:

- Joins
- Aggregations
- GROUP BY
- CTE
- Window Functions
- DENSE_RANK()
- NTILE()
- LAG()
- Running Totals
- Customer Segmentation
- Cohort Analysis
- Year-over-Year Comparison

---

# 💻 CLI Reporting Tool

The command-line tool allows users to generate reports.

Available reports:

- Daily
- Weekly
- Monthly

Displays:

- Total Orders
- Revenue
- Unique Customers
- Top Products

---

# 🧪 Edge Case Testing

Implemented test cases for:

- Invalid Order IDs
- Discount > 100
- Quantity = 0
- Future Dates

---

# 📷 Sample Outputs

Screenshots are available in:

```
output/sample_reports/
```

---

# ▶️ How to Run

### Generate Data

```bash
python scripts/generate_data.py
```

### Clean Data

```bash
python scripts/clean_data.py
```

### Load Database

```bash
python scripts/load_database.py
```

### Run CLI Tool

```bash
python scripts/report_cli.py
```

### Run Edge Case Tests

```bash
python tests/test_edge_cases.py
```

---

# 📌 Future Improvements

- Dashboard using Power BI
- Streamlit Web Application
- Machine Learning for Sales Prediction
- Fraud Detection
- Cloud Deployment

---

# 👨‍💻 Author

**Naman Garg**

B.Tech CSE (Cloud Computing & Information Security)

Celebal Technologies Internship – Week 8 Mini Project