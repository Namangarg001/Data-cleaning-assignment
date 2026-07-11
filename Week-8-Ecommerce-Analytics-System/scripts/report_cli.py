# ==========================================================
# E-Commerce Order Analytics System
# Command Line Reporting Tool
# ==========================================================

import sqlite3

from tabulate import tabulate

# ==========================================================
# Connect Database
# ==========================================================

connection = sqlite3.connect("database/ecommerce.db")

cursor = connection.cursor()

print("\n========================================")
print(" E-Commerce Analytics Reporting System ")
print("========================================\n")

# ==========================================================
# User Input
# ==========================================================

report_type = input(
    "Enter Report Type (daily / weekly / monthly): "
).lower()

start_date = input(
    "Enter Start Date (YYYY-MM-DD): "
)

end_date = input(
    "Enter End Date (YYYY-MM-DD): "
)

# ==========================================================
# Total Orders
# ==========================================================

cursor.execute("""

SELECT COUNT(*)

FROM orders

WHERE DATE(order_date)
BETWEEN ? AND ?

""",(start_date,end_date))

total_orders = cursor.fetchone()[0]

# ==========================================================
# Revenue
# ==========================================================

cursor.execute("""

SELECT

ROUND(

SUM(

oi.quantity *

p.unit_price *

(1-oi.discount_percent/100.0)

),

2

)

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

WHERE DATE(o.order_date)

BETWEEN ? AND ?

""",(start_date,end_date))

revenue = cursor.fetchone()[0]

# ==========================================================
# Unique Customers
# ==========================================================

cursor.execute("""

SELECT

COUNT(DISTINCT customer_id)

FROM orders

WHERE DATE(order_date)

BETWEEN ? AND ?

""",(start_date,end_date))

customers = cursor.fetchone()[0]

# ==========================================================
# Top 3 Products
# ==========================================================

cursor.execute("""

SELECT

p.product_name,

SUM(oi.quantity) AS quantity

FROM order_items oi

JOIN orders o

ON oi.order_id=o.order_id

JOIN products p

ON oi.product_id=p.product_id

WHERE DATE(o.order_date)

BETWEEN ? AND ?

GROUP BY p.product_name

ORDER BY quantity DESC

LIMIT 3

""",(start_date,end_date))

top_products = cursor.fetchall()

# ==========================================================
# Print Summary
# ==========================================================

print("\n==============================")
print("SUMMARY REPORT")
print("==============================\n")

summary = [

["Report Type",report_type],

["Start Date",start_date],

["End Date",end_date],

["Total Orders",total_orders],

["Revenue",revenue],

["Unique Customers",customers]

]

print(tabulate(summary,tablefmt="grid"))

print("\nTop 3 Products\n")

print(

tabulate(

top_products,

headers=["Product","Quantity"],

tablefmt="grid"

)

)

# ==========================================================
# Previous Period Comparison
# ==========================================================

print("\nPrevious Period Comparison feature can be extended.")

connection.close()

print("\nDatabase Connection Closed.")