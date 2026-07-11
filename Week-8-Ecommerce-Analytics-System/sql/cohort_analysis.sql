-- ==========================================================
-- E-Commerce Order Analytics System
-- Advanced CTE & Cohort Analysis
-- ==========================================================

-------------------------------------------------------------
-- 1. Monthly Revenue Per Customer
-------------------------------------------------------------

WITH MonthlyRevenue AS (

    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,

        SUM(
            oi.quantity *
            p.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o

    JOIN order_items oi
        ON o.order_id = oi.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    GROUP BY
        o.customer_id,
        order_month
)

SELECT

    customer_id,

    order_month,

    ROUND(revenue,2) AS revenue,

    CASE

        WHEN revenue > 10000 THEN 'High'

        WHEN revenue BETWEEN 5000 AND 10000 THEN 'Medium'

        ELSE 'Low'

    END AS customer_segment

FROM MonthlyRevenue

ORDER BY
customer_id,
order_month;

-------------------------------------------------------------
-- 2. Customer Count Per Segment
-------------------------------------------------------------

WITH MonthlyRevenue AS (

SELECT

o.customer_id,

strftime('%Y-%m',o.order_date) AS month,

SUM(

oi.quantity*

p.unit_price*

(1-oi.discount_percent/100.0)

)

AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY
o.customer_id,
month

),

CustomerSegment AS(

SELECT

month,

CASE

WHEN revenue>10000 THEN 'High'

WHEN revenue BETWEEN 5000 AND 10000 THEN 'Medium'

ELSE 'Low'

END AS segment

FROM MonthlyRevenue

)

SELECT

month,

segment,

COUNT(*) AS total_customers

FROM CustomerSegment

GROUP BY
month,
segment

ORDER BY
month;

-------------------------------------------------------------
-- 3. Year Over Year Revenue
-------------------------------------------------------------

WITH Revenue AS(

SELECT

strftime('%Y',o.order_date) AS year,

strftime('%m',o.order_date) AS month,

SUM(

oi.quantity*

p.unit_price*

(1-oi.discount_percent/100.0)

)

AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

GROUP BY
year,
month

)

SELECT

year,

month,

ROUND(revenue,2),

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

)

AS prev_year_revenue,

ROUND(

(

revenue-

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

)

)

/

LAG(revenue)

OVER(

PARTITION BY month

ORDER BY year

)

*100,

2

)

AS yoy_growth_percent

FROM Revenue;

-------------------------------------------------------------
-- 4. First Purchased Category
-------------------------------------------------------------

WITH PurchaseHistory AS(

SELECT

o.customer_id,

p.category,

o.order_date,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date

)

AS rn

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

)

SELECT

customer_id,

category

AS first_category

FROM PurchaseHistory

WHERE rn=1;

-------------------------------------------------------------
-- 5. Most Recent Purchased Category
-------------------------------------------------------------

WITH PurchaseHistory AS(

SELECT

o.customer_id,

p.category,

o.order_date,

ROW_NUMBER()

OVER(

PARTITION BY o.customer_id

ORDER BY o.order_date DESC

)

AS rn

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

JOIN products p

ON oi.product_id=p.product_id

)

SELECT

customer_id,

category

AS latest_category

FROM PurchaseHistory

WHERE rn=1;

-------------------------------------------------------------
-- 6. Cohort Analysis
-------------------------------------------------------------

WITH customer_cohort AS (

SELECT

customer_id,

strftime('%Y-%m',MIN(order_date))

AS cohort_month

FROM orders

GROUP BY customer_id

),

cohort_orders AS (

SELECT

c.customer_id,

c.cohort_month,

strftime('%Y-%m',o.order_date)

AS order_month

FROM customer_cohort c

JOIN orders o

ON c.customer_id=o.customer_id

)

SELECT

cohort_month,

order_month,

COUNT(DISTINCT customer_id)

AS customers

FROM cohort_orders

GROUP BY

cohort_month,

order_month

ORDER BY

cohort_month,

order_month;