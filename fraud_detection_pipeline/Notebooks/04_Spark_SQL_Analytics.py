# Databricks notebook source
# =========================================================
# 04_Spark_SQL_Analytics.py
# Purpose: Aggregated business insights using Spark SQL
# Generates fraud summary and account-level fraud analysis
# from the Gold layer.
# =========================================================

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT fraud_status,
# MAGIC        COUNT(*) AS txn_count,
# MAGIC        ROUND(SUM(amount), 2) AS total_amount,
# MAGIC        ROUND(AVG(amount), 2) AS avg_amount
# MAGIC FROM gold_fraud_transactions
# MAGIC GROUP BY fraud_status

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT account_id, customer_name,
# MAGIC        COUNT(*) AS total_txns,
# MAGIC        SUM(CASE WHEN fraud_status = 'fraud' THEN 1 ELSE 0 END) AS fraud_txns,
# MAGIC        ROUND(SUM(CASE WHEN fraud_status = 'fraud' THEN amount ELSE 0 END), 2) AS fraud_amount
# MAGIC FROM gold_fraud_transactions
# MAGIC GROUP BY account_id, customer_name
# MAGIC HAVING fraud_txns > 0
# MAGIC ORDER BY fraud_txns DESC

# COMMAND ----------

# Save both summaries as permanent Gold tables
summary_df = spark.sql("""
    SELECT fraud_status,
           COUNT(*) AS txn_count,
           ROUND(SUM(amount), 2) AS total_amount,
           ROUND(AVG(amount), 2) AS avg_amount
    FROM gold_fraud_transactions
    GROUP BY fraud_status
""")
summary_df.write.format("delta").mode("overwrite").saveAsTable("gold_fraud_summary")

account_summary_df = spark.sql("""
    SELECT account_id, customer_name,
           COUNT(*) AS total_txns,
           SUM(CASE WHEN fraud_status = 'fraud' THEN 1 ELSE 0 END) AS fraud_txns,
           ROUND(SUM(CASE WHEN fraud_status = 'fraud' THEN amount ELSE 0 END), 2) AS fraud_amount
    FROM gold_fraud_transactions
    GROUP BY account_id, customer_name
    HAVING fraud_txns > 0
    ORDER BY fraud_txns DESC
""")
account_summary_df.write.format("delta").mode("overwrite").saveAsTable("gold_account_summary")

print("Gold summary tables created successfully!")
