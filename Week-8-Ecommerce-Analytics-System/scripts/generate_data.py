import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Create a Faker object to generate fake data
fake = Faker()

# Set a random seed so the generated data is reproducible
random.seed(42)
Faker.seed(42)

os.makedirs("data/raw", exist_ok=True)
    
# ==========================================================
# Project Constants
# ==========================================================

# Number of records to generate
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 500
NUM_ORDERS = 1000
NUM_ORDER_ITEMS = 3000

# Customer Types
CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

# Region Codes
REGIONS = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]

# Order Status
ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

# ==========================================================
# Product Categories and Subcategories
# ==========================================================

PRODUCT_CATEGORIES = {

    "Electronics": [
        "Laptop",
        "Mobile",
        "Headphones",
        "Smart Watch"
    ],

    "Clothing": [
        "Shirt",
        "Jeans",
        "Shoes",
        "Jacket"
    ],

    "Home": [
        "Table",
        "Chair",
        "Lamp",
        "Sofa"
    ],

    "Books": [
        "Novel",
        "Biography",
        "Programming",
        "Comics"
    ],

    "Sports": [
        "Cricket Bat",
        "Football",
        "Gym Bag",
        "Tennis Racket"
    ],

    "Beauty": [
        "Face Wash",
        "Lipstick",
        "Perfume",
        "Shampoo"
    ]

}

# ==========================================================
# Product Brands
# ==========================================================

PRODUCT_BRANDS = [

    "Samsung",
    "Apple",
    "Dell",
    "HP",
    "Lenovo",
    "Sony",
    "Nike",
    "Adidas",
    "Puma",
    "Boat",
    "Philips",
    "Loreal",
    "Lakme",
    "Mamaearth"

]

# ==========================================================
# Function: Generate Customers
# ==========================================================

def generate_customers():
    """
    Generates customer data with intentional data quality issues.

    Output:
        data/raw/customers.csv
    """

    print("Generating customers...")

    # Empty list to store customer records
    customers = []
        # Generate customer records
    for customer_id in range(1, NUM_CUSTOMERS + 1):

        # Generate customer name
        customer_name = fake.name()

        # Generate customer email
        email = fake.email()

        # Generate registration date
        registration_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        # Random customer type
        customer_type = random.choice(CUSTOMER_TYPES)

        # Random region
        region_code = random.choice(REGIONS)
                # --------------------------------------------------
        # Introduce Invalid Emails (2%)
        # --------------------------------------------------

        if random.random() < 0.02:

            # Remove '@' from email
            email = email.replace("@", "")

                    # Store customer record
        customers.append({

            "customer_id": customer_id,
            "customer_name": customer_name,
            "email": email,
            "registration_date": registration_date,
            "customer_type": customer_type,
            "region_code": region_code

        })
    # ==========================================================
    # Convert List to DataFrame
    # ==========================================================

    customers_df = pd.DataFrame(customers)

    # ==========================================================
    # Save DataFrame as CSV
    # ==========================================================

    customers_df.to_csv(
        "data/raw/customers.csv",
        index=False
    )

    print("✅ customers.csv generated successfully!")

    return customers_df      
# ==========================================================
# Main Function
# ==========================================================

if __name__ == "__main__":

    generate_customers()


# ==========================================================
# Function: Generate Products
# ==========================================================

def generate_products():

    """
    Generates product data.

    Output:
        data/raw/products.csv
    """

    print("Generating products...")

    products = []

    for product_id in range(1, NUM_PRODUCTS + 1):

        category = random.choice(list(PRODUCT_CATEGORIES.keys()))

        subcategory = random.choice(PRODUCT_CATEGORIES[category])

        brand = random.choice(PRODUCT_BRANDS)

        product_name = f"{brand} {subcategory}"

        cost_price = random.randint(200, 50000)

        unit_price = cost_price + random.randint(100, 8000)

        chance = random.random()

        if chance < 0.02:
            product_name = product_name.upper()

        elif chance < 0.04:
            product_name = "  " + product_name + "  "

        elif chance < 0.05:
            product_name = product_name.lower()

        # ⭐ VERY IMPORTANT ⭐
        # This must be OUTSIDE the if block
        products.append({

            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price,
            "unit_price": unit_price

        })

    products_df = pd.DataFrame(products)

    products_df.to_csv(
        "data/raw/products.csv",
        index=False
    )

    print("✅ products.csv generated successfully!")

    return products_df
if __name__ == "__main__":

    generate_customers()
    generate_products()

    # ==========================================================
# Function: Generate Orders
# ==========================================================

def generate_orders():

    print("Generating orders...")

    orders = []

    for order_id in range(1, NUM_ORDERS + 1):

        customer_id = random.randint(1, NUM_CUSTOMERS)

        if random.random() < 0.05:
            customer_id = None

        order_date = fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )

        order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")

        if random.random() < 0.05:
            order_date = datetime.strptime(
                order_date,
                "%Y-%m-%d %H:%M:%S"
            ).strftime("%d-%m-%Y")

        status = random.choice(ORDER_STATUS)

        # ← This MUST be inside the for loop
        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status
        })

    orders_df = pd.DataFrame(orders)

    orders_df.to_csv(
        "data/raw/orders.csv",
        index=False
    )

    print("orders.csv generated successfully!")

    return orders_df

if __name__ == "__main__":

    generate_customers()
    generate_products()
    generate_orders()

    # ==========================================================
# Function: Generate Order Items
# ==========================================================

def generate_order_items():
    """
    Generates order items data.

    Output:
        data/raw/order_items.csv
    """

    print("Generating order items...")

    # Empty list
    order_items = []

    # Generate order items
    for order_item_id in range(1, NUM_ORDER_ITEMS + 1):

        # Random order
        order_id = random.randint(1, NUM_ORDERS)

        # Random product
        product_id = random.randint(1, NUM_PRODUCTS)

        # Quantity
        quantity = random.randint(1, 5)

        # Discount
        discount_percent = random.randint(0, 100)

        # 3% negative quantity
        if random.random() < 0.03:
            quantity = -quantity

        # Store order item
        order_items.append({

            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "discount_percent": discount_percent

        })

    # Convert to DataFrame
    order_items_df = pd.DataFrame(order_items)

    # Save CSV
    order_items_df.to_csv(
        "data/raw/order_items.csv",
        index=False
    )

    print("✅ order_items.csv generated successfully!")

    return order_items_df
if __name__ == "__main__":

    generate_customers()

    generate_products()

    generate_orders()

    generate_order_items()