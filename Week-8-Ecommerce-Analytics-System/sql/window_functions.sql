-- ==========================================================
-- E-Commerce Order Analytics System
-- Window Functions & Advanced SQL Queries
-- ==========================================================

-------------------------------------------------------------
-- 1. Running Total of Revenue by Region
-------------------------------------------------------------

WITH DailyRevenue AS
(
    SELECT

        c.region_code,

        DATE(o.order_date) AS order_date,

        SUM(
            oi.quantity *
            p.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS daily_revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    GROUP BY
        c.region_code,
        DATE(o.order_date)
)

SELECT

    region_code,

    order_date,

    ROUND(daily_revenue,2) AS daily_revenue,

    ROUND(

        SUM(daily_revenue)
        OVER(
            PARTITION BY region_code
            ORDER BY order_date
        ),

        2

    ) AS running_total

FROM DailyRevenue;

-------------------------------------------------------------
-- 2. Rank Products by Revenue
-------------------------------------------------------------

SELECT

    p.category,

    p.product_name,

    ROUND(

        SUM(
            oi.quantity *
            p.unit_price *
            (1-oi.discount_percent/100.0)
        ),

        2

    ) AS total_revenue,

    DENSE_RANK() OVER(

        PARTITION BY p.category

        ORDER BY

        SUM(
            oi.quantity *
            p.unit_price *
            (1-oi.discount_percent/100.0)
        ) DESC

    ) AS rank_in_category

FROM products p

JOIN order_items oi

ON p.product_id=oi.product_id

GROUP BY

p.category,
p.product_name;

-------------------------------------------------------------
-- 3. Days Between Consecutive Orders
-------------------------------------------------------------

SELECT

customer_id,

order_date,

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

AS previous_order_date,

JULIANDAY(order_date)-

JULIANDAY(

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

)

AS days_gap

FROM orders;

-------------------------------------------------------------
-- 4. Customers At Risk
-------------------------------------------------------------

WITH gaps AS(

SELECT

customer_id,

JULIANDAY(order_date)-

JULIANDAY(

LAG(order_date)

OVER(

PARTITION BY customer_id

ORDER BY order_date

)

)

AS gap

FROM orders

)

SELECT

customer_id,

ROUND(AVG(gap),2) AS avg_gap,

CASE

WHEN AVG(gap)>30

THEN 'At Risk'

ELSE 'Active'

END AS customer_status

FROM gaps

GROUP BY customer_id;

-------------------------------------------------------------
-- 5. Customer Segmentation Using NTILE
-------------------------------------------------------------

WITH customer_value AS(

SELECT

c.customer_id,

SUM(

oi.quantity*

p.unit_price*

(1-oi.discount_percent/100.0)

)

AS total_value

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY c.customer_id

)

SELECT

customer_id,

ROUND(total_value,2),

NTILE(4)

OVER(

ORDER BY total_value DESC

)

AS quartile,

CASE

WHEN NTILE(4) OVER(ORDER BY total_value DESC)=1
THEN 'Platinum'

WHEN NTILE(4) OVER(ORDER BY total_value DESC)=2
THEN 'Gold'

WHEN NTILE(4) OVER(ORDER BY total_value DESC)=3
THEN 'Silver'

ELSE 'Bronze'

END AS quartile_label

FROM customer_value;