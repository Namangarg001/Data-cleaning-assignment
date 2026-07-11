# ==========================================================
# E-Commerce Order Analytics System
# Load Cleaned Data into SQLite Database
# ==========================================================

import sqlite3
import pandas as pd
import os

# ==========================================================
# Database Path
# ==========================================================

DATABASE_PATH = "database/ecommerce.db"
SCHEMA_PATH = "sql/schema.sql"

# ==========================================================
# Connect Database
# ==========================================================

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

print("Connected to SQLite Database")

# ==========================================================
# Execute Schema File
# ==========================================================

with open(SCHEMA_PATH, "r") as file:
    schema = file.read()

cursor.executescript(schema)

print("Database Schema Created Successfully")

# ==========================================================
# Read Cleaned CSV Files
# ==========================================================

customers = pd.read_csv("data/cleaned/customers_clean.csv")

products = pd.read_csv("data/cleaned/products_clean.csv")

orders = pd.read_csv("data/cleaned/orders_clean.csv")

order_items = pd.read_csv("data/cleaned/order_items_clean.csv")

# ==========================================================
# Insert Customers
# ==========================================================

customers.to_sql(
    "customers",
    connection,
    if_exists="append",
    index=False
)

print("Customers Loaded")

# ==========================================================
# Insert Products
# ==========================================================

products.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False
)

print("Products Loaded")

# ==========================================================
# Insert Orders
# ==========================================================

orders.to_sql(
    "orders",
    connection,
    if_exists="append",
    index=False
)

print("Orders Loaded")

# ==========================================================
# Insert Order Items
# ==========================================================

order_items.to_sql(
    "order_items",
    connection,
    if_exists="append",
    index=False
)

print("Order Items Loaded")

# ==========================================================
# Verify Row Counts
# ==========================================================

print("\n========== DATABASE SUMMARY ==========\n")

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    rows = cursor.fetchone()[0]

    print(f"{table:<15} : {rows}")

# ==========================================================
# Commit Changes
# ==========================================================

connection.commit()

connection.close()

print("\nDatabase Loaded Successfully.")