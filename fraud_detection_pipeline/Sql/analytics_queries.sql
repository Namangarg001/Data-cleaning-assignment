-- =========================================================
-- analytics_queries.sql
-- Aggregated reporting queries run on the Gold layer
-- (gold_fraud_transactions table)
-- =========================================================

-- 1. Overall fraud vs normal summary
SELECT fraud_status,
       COUNT(*) AS txn_count,
       ROUND(SUM(amount), 2) AS total_amount,
       ROUND(AVG(amount), 2) AS avg_amount
FROM gold_fraud_transactions
GROUP BY fraud_status;

-- 2. Account-level fraud analysis
SELECT account_id, customer_name,
       COUNT(*) AS total_txns,
       SUM(CASE WHEN fraud_status = 'fraud' THEN 1 ELSE 0 END) AS fraud_txns,
       ROUND(SUM(CASE WHEN fraud_status = 'fraud' THEN amount ELSE 0 END), 2) AS fraud_amount
FROM gold_fraud_transactions
GROUP BY account_id, customer_name
HAVING fraud_txns > 0
ORDER BY fraud_txns DESC;
