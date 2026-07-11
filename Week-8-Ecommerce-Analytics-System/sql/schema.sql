-- ==========================================================
-- E-Commerce Order Analytics System
-- Database Schema
-- ==========================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-------------------------------------------------------------
-- Customers
-------------------------------------------------------------

CREATE TABLE customers(

    customer_id INTEGER PRIMARY KEY,

    customer_name TEXT NOT NULL,

    email TEXT NOT NULL,

    registration_date DATE,

    customer_type TEXT CHECK(
        customer_type IN
        ('REGULAR','PREMIUM','VIP')
    ),

    region_code TEXT

);

-------------------------------------------------------------
-- Products
-------------------------------------------------------------

CREATE TABLE products(

    product_id INTEGER PRIMARY KEY,

    product_name TEXT NOT NULL,

    category TEXT,

    subcategory TEXT,

    cost_price REAL,

    unit_price REAL

);

-------------------------------------------------------------
-- Orders
-------------------------------------------------------------

CREATE TABLE orders(

    order_id INTEGER PRIMARY KEY,

    customer_id INTEGER,

    order_date TEXT,

    status TEXT CHECK(

        status IN(

            'PLACED',

            'SHIPPED',

            'DELIVERED',

            'CANCELLED',

            'RETURNED'

        )

    ),

    FOREIGN KEY(customer_id)

    REFERENCES customers(customer_id)

);

-------------------------------------------------------------
-- Order Items
-------------------------------------------------------------

CREATE TABLE order_items(

    order_item_id INTEGER PRIMARY KEY,

    order_id INTEGER,

    product_id INTEGER,

    quantity INTEGER,

    discount_percent REAL,

    FOREIGN KEY(order_id)

    REFERENCES orders(order_id),

    FOREIGN KEY(product_id)

    REFERENCES products(product_id)

);