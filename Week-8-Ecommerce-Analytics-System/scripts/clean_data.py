# ==========================================================
# Import Required Libraries
# ==========================================================

import os
import re
import pandas as pd
# ==========================================================
# Create Output Folder
# ==========================================================

os.makedirs("data/cleaned", exist_ok=True)
# ==========================================================
# Load Raw CSV Files
# ==========================================================

customers_df = pd.read_csv("data/raw/customers.csv")

products_df = pd.read_csv("data/raw/products.csv")

orders_df = pd.read_csv("data/raw/orders.csv")

order_items_df = pd.read_csv("data/raw/order_items.csv")
# ==========================================================
# Issues Report
# ==========================================================

issues = []
import os
import re
import pandas as pd

os.makedirs("data/cleaned", exist_ok=True)

customers_df = pd.read_csv("data/raw/customers.csv")

products_df = pd.read_csv("data/raw/products.csv")

orders_df = pd.read_csv("data/raw/orders.csv")

order_items_df = pd.read_csv("data/raw/order_items.csv")

issues = []

# ==========================================================
# Function: Clean Orders
# ==========================================================

def clean_orders():
    """
    Cleans the orders dataset by:
    1. Fixing incorrect date formats.
    2. Handling missing customer IDs.
    """

    print("Cleaning orders...")

    global orders_df

        # Convert all order dates into proper datetime format
    orders_df["order_date"] = pd.to_datetime(
        orders_df["order_date"],
        errors="coerce",
        dayfirst=True
    )
        # Count invalid dates
    invalid_dates = orders_df["order_date"].isna().sum()

    issues.append(
        f"Invalid order dates found: {invalid_dates}"
    )

        # Count missing customer IDs
    missing_customer = orders_df["customer_id"].isna().sum()

    issues.append(
        f"Missing customer IDs: {missing_customer}"
    )

    # Replace NULL customer IDs with -1
    orders_df["customer_id"] = orders_df["customer_id"].fillna(-1)

        # Save cleaned orders
    orders_df.to_csv(
        "data/cleaned/orders_clean.csv",
        index=False
    )

    print("✅ orders_clean.csv created.")

if __name__ == "__main__":

    clean_orders()

    # ==========================================================
# Function: Clean Products
# ==========================================================

def clean_products():
    """
    Cleans the products dataset by:
    1. Removing extra spaces.
    2. Converting product names to Title Case.
    """

    print("Cleaning products...")

    global products_df
        # Remove leading and trailing spaces
    products_df["product_name"] = (
        products_df["product_name"]
        .astype(str)
        .str.strip()
    )

        # Convert product names to Title Case
    products_df["product_name"] = (
        products_df["product_name"]
        .str.title()
    )
        # Count total products cleaned
    cleaned_products = len(products_df)

    issues.append(
        f"Products cleaned: {cleaned_products}"
    )
        # Save cleaned products
    products_df.to_csv(
        "data/cleaned/products_clean.csv",
        index=False
    )

    print("✅ products_clean.csv created.")
if __name__ == "__main__":

    clean_orders()

    clean_products()

    # ==========================================================
# Function: Validate Emails
# ==========================================================

def validate_emails():
    """
    Finds invalid email addresses using Regular Expression.
    Returns a list of customer IDs having invalid emails.
    """

    print("Validating customer emails...")

    global customers_df

    # Regular Expression for valid email
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    # Find invalid emails
    invalid_emails = customers_df[
        ~customers_df["email"].astype(str).str.match(email_pattern)
    ]

    # Save issue
    issues.append(
        f"Invalid Emails Found : {len(invalid_emails)}"
    )

    # Save cleaned customer file
    customers_df.to_csv(
        "data/cleaned/customers_clean.csv",
        index=False
    )

    print("✅ customers_clean.csv created.")

    return invalid_emails["customer_id"].tolist()

# ==========================================================
# Function: Check Referential Integrity
# ==========================================================

def check_referential_integrity():
    """
    Finds order_items having invalid order_id.
    """

    print("Checking Referential Integrity...")

    global order_items_df
    global orders_df

    invalid_orders = order_items_df[
        ~order_items_df["order_id"].isin(
            orders_df["order_id"]
        )
    ]

    issues.append(
        f"Invalid Order References : {len(invalid_orders)}"
    )

    # Save cleaned order_items file
    order_items_df.to_csv(
        "data/cleaned/order_items_clean.csv",
        index=False
    )

    print("✅ order_items_clean.csv created.")

    return invalid_orders

# ==========================================================
# Function: Generate Issues Report
# ==========================================================

def generate_issue_report():
    """
    Saves all detected issues into issues_report.txt
    """

    print("Generating Issues Report...")

    with open(
        "data/cleaned/issues_report.txt",
        "w"
    ) as file:

        file.write("E-Commerce Analytics System\n")
        file.write("==============================\n\n")

        for issue in issues:
            file.write(issue + "\n")

    print("✅ issues_report.txt created.")

    # ==========================================================
# Main Function
# ==========================================================

if __name__ == "__main__":

    clean_orders()

    clean_products()

    validate_emails()

    check_referential_integrity()

    generate_issue_report()

    print("\n🎉 Data Cleaning Completed Successfully!")