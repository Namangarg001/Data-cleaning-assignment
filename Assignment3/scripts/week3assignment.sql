USE superstore_db;

SELECT *
FROM superstore_raw
LIMIT 10;

--  Create Customers Table

CREATE TABLE customers (
    customer_id VARCHAR(30),
    customer_name VARCHAR(100),
    segment VARCHAR(50)
);

--  Insert Unique Customers
-- Using SELECT DISTINCT

INSERT INTO customers
SELECT DISTINCT
    `Customer ID`,
    `Customer Name`,
    Segment
FROM superstore_raw;

-- Verify Customers Data
SELECT *
FROM customers
LIMIT 10;

-- STEP 5: Create Orders Table

CREATE TABLE orders (
    row_id INT,
    order_id VARCHAR(50),
    order_date VARCHAR(50),
    ship_date VARCHAR(50),
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    sales DOUBLE,
    quantity INT,
    discount DOUBLE,
    profit DOUBLE
);

-- Insert Orders Data
-- Using SELECT DISTINCT

INSERT INTO orders
SELECT DISTINCT
    `Row ID`,
    `Order ID`,
    `Order Date`,
    `Ship Date`,
    `Ship Mode`,
    `Customer ID`,
    Sales,
    Quantity,
    Discount,
    Profit
FROM superstore_raw;

-- Verify Orders Data

SELECT *
FROM orders
LIMIT 10;

-- STEP 8: Create Products Table

CREATE TABLE products (
    product_id VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name TEXT
);
-- STEP 9: Insert Unique Products
-- Using SELECT DISTINCT


INSERT INTO products
SELECT DISTINCT
    `Product ID`,
    Category,
    `Sub-Category`,
    `Product Name`
FROM superstore_raw;

-- Verify Products Table
SELECT *
FROM products
LIMIT 10;

SHOW TABLES;

-- Find orders where sales > average sales
SELECT *
FROM orders
WHERE sales > (
    SELECT AVG(sales) FROM orders
);

-- Highest sales order for each customer
SELECT o.*
FROM orders o
JOIN (
    SELECT customer_id, MAX(sales) AS max_sales
    FROM orders
    GROUP BY customer_id
) m
ON o.customer_id = m.customer_id
AND o.sales = m.max_sales;


-- Calculate total sales for each customer
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT * FROM customer_sales;

-- Customers whose total sales > average customer sales
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales
WHERE total_sales > (
    SELECT AVG(total_sales) FROM customer_sales
);

-- Rank customers based on total sales
SELECT
    customer_id,
    SUM(sales) AS total_sales,
    RANK() OVER (ORDER BY SUM(sales) DESC) AS rank_position
FROM orders
GROUP BY customer_id;

-- Assign row numbers to orders within each customer
SELECT
    customer_id,
    order_id,
    sales,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY sales DESC
    ) AS row_num
FROM orders;

-- Top 3 customers based on total sales
SELECT *
FROM (
    SELECT
        customer_id,
        SUM(sales) AS total_sales,
        RANK() OVER (ORDER BY SUM(sales) DESC) AS rnk
    FROM orders
    GROUP BY customer_id
) t
WHERE rnk <= 3; 

-- Final query combining JOIN + CTE + Window Function

WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)

SELECT
    c.customer_name,
    cs.total_sales,
    RANK() OVER (ORDER BY cs.total_sales DESC) AS rank_position
FROM customer_sales cs
JOIN customers c
ON cs.customer_id = c.customer_id;

-- Top 5 customers
SELECT *
FROM (
    SELECT
        customer_id,
        SUM(sales) AS total_sales,
        RANK() OVER (ORDER BY SUM(sales) DESC) AS rnk
    FROM orders
    GROUP BY customer_id
) t
WHERE rnk <= 5;

-- Customers with only one order
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) = 1;

-- Customers with above average total sales
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT *
FROM customer_sales
WHERE total_sales > (
    SELECT AVG(total_sales) FROM customer_sales
);

-- Highest order value per customer
SELECT *
FROM orders o
WHERE sales = (
    SELECT MAX(sales)
    FROM orders
    WHERE customer_id = o.customer_id
);	