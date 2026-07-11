-- ==========================================================
-- E-Commerce Order Analytics System
-- Basic SQL Queries
-- ==========================================================

-------------------------------------------------------------
-- 1. Total Revenue Per Category
-------------------------------------------------------------

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            p.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-------------------------------------------------------------
-- 2. Top 10 Customers By Revenue
-------------------------------------------------------------

SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(
            oi.quantity *
            p.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC
LIMIT 10;


-------------------------------------------------------------
-- 3. Month Wise Order Count
-------------------------------------------------------------

SELECT

    strftime('%Y-%m', order_date) AS order_month,

    COUNT(*) AS total_orders

FROM orders

GROUP BY order_month

ORDER BY order_month;


-------------------------------------------------------------
-- 4. Revenue Per Customer
-------------------------------------------------------------

SELECT

    c.customer_name,

    ROUND(

        SUM(

            oi.quantity *

            p.unit_price *

            (1-oi.discount_percent/100.0)

        ),

        2

    ) AS revenue

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY c.customer_name

ORDER BY revenue DESC;


-------------------------------------------------------------
-- 5. Revenue Per Month
-------------------------------------------------------------

SELECT

    strftime('%Y-%m',o.order_date) AS month,

    ROUND(

        SUM(

            oi.quantity*

            p.unit_price*

            (1-oi.discount_percent/100.0)

        ),

        2

    ) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY month

ORDER BY month;


-------------------------------------------------------------
-- 6. Average Order Value (AOV)
-------------------------------------------------------------

SELECT

    ROUND(

        AVG(order_total),

        2

    ) AS average_order_value

FROM

(

SELECT

    o.order_id,

    SUM(

        oi.quantity*

        p.unit_price*

        (1-oi.discount_percent/100.0)

    ) AS order_total

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY o.order_id

);