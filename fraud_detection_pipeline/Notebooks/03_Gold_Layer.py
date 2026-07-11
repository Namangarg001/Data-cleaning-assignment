# Databricks notebook source
# =========================================================
# 03_Gold_Layer.py
# Purpose: Fraud detection logic (Gold Layer)
# Joins enriched transactions with the fraud watchlist and
# classifies each transaction as "fraud" or "normal".
# =========================================================

# COMMAND ----------

from pyspark.sql.functions import when, col

silver_df = spark.table("silver_transactions_enriched")

# Watchlist -> only account_id, renamed to avoid join collisions
watchlist_clean = spark.table("bronze_watchlist") \
    .dropna(subset=["account_id"]) \
    .select(col("account_id").alias("flagged_account"), "fraud_type", "flagged_date")

# Left join silver transactions with the watchlist
gold_df = silver_df.join(
    watchlist_clean,
    silver_df.account_id == watchlist_clean.flagged_account,
    how="left"
)

# Classify fraud vs normal
gold_df = gold_df.withColumn(
    "fraud_status",
    when(col("flagged_account").isNotNull(), "fraud").otherwise("normal")
)

gold_df.show(10)
print("Total transactions:", gold_df.count())
print("Fraud transactions:", gold_df.filter(col("fraud_status") == "fraud").count())

# COMMAND ----------

gold_df.write.format("delta").mode("overwrite").saveAsTable("gold_fraud_transactions")

print("Gold table created successfully!")
