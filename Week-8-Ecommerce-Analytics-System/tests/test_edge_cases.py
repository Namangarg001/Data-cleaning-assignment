# ==========================================================
# E-Commerce Order Analytics System
# Edge Case Testing
# ==========================================================

import pandas as pd


# ==========================================================
# Test 1
# Invalid Order ID
# ==========================================================

def test_invalid_order_id():

    print("\nTest 1 : Invalid Order ID")

    orders = pd.read_csv("data/cleaned/orders_clean.csv")

    order_items = pd.read_csv("data/cleaned/order_items_clean.csv")

    invalid = order_items[
        ~order_items["order_id"].isin(orders["order_id"])
    ]

    print(f"Invalid Order References : {len(invalid)}")


# ==========================================================
# Test 2
# Discount Greater Than 100
# ==========================================================

def test_invalid_discount():

    print("\nTest 2 : Discount > 100")

    order_items = pd.read_csv("data/cleaned/order_items_clean.csv")

    invalid = order_items[
        order_items["discount_percent"] > 100
    ]

    print(f"Invalid Discounts : {len(invalid)}")


# ==========================================================
# Test 3
# Quantity Equal To Zero
# ==========================================================

def test_zero_quantity():

    print("\nTest 3 : Quantity = 0")

    order_items = pd.read_csv("data/cleaned/order_items_clean.csv")

    invalid = order_items[
        order_items["quantity"] == 0
    ]

    print(f"Zero Quantity Records : {len(invalid)}")


# ==========================================================
# Test 4
# Future Order Dates
# ==========================================================

def test_future_dates():

    print("\nTest 4 : Future Order Dates")

    orders = pd.read_csv("data/cleaned/orders_clean.csv")

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    future = orders[
        orders["order_date"] > pd.Timestamp.today()
    ]

    print(f"Future Orders : {len(future)}")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("\n==============================")
    print("EDGE CASE TESTING")
    print("==============================")

    test_invalid_order_id()

    test_invalid_discount()

    test_zero_quantity()

    test_future_dates()

    print("\nAll Tests Completed Successfully.")