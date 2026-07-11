# Databricks notebook source
# =========================================================
# 02_Silver_Layer.py
# Purpose: Data cleaning and enrichment (Silver Layer)
# Cleans nulls, casts types, and joins accounts + transactions
# on account_id to build an enriched dataset.
# =========================================================

# COMMAND ----------

from pyspark.sql.functions import col, to_date, trim

# ---- Clean accounts table ----
accounts_clean = spark.table("bronze_accounts") \
    .dropna(subset=["account_id"]) \
    .withColumn("opening_date", to_date(col("opening_date"))) \
    .withColumn("credit_limit", col("credit_limit").cast("double")) \
    .withColumn("customer_name", trim(col("customer_name")))

# Fill missing credit_limit values with 0
accounts_clean = accounts_clean.fillna({"credit_limit": 0})

# ---- Clean transactions table ----
transactions_clean = spark.table("bronze_transactions") \
    .dropna(subset=["txn_id", "account_id"]) \
    .withColumn("txn_date", to_date(col("txn_date"))) \
    .withColumn("amount", col("amount").cast("double"))

# Fill missing merchant values with "Unknown"
transactions_clean = transactions_clean.fillna({"merchant": "Unknown"})

# COMMAND ----------

# ---- Join transactions with accounts (enrichment) ----
silver_df = transactions_clean.join(accounts_clean, on="account_id", how="left")

silver_df.show(5)
print("Total rows:", silver_df.count())

# COMMAND ----------

silver_df.write.format("delta").mode("overwrite").saveAsTable("silver_transactions_enriched")

print("Silver table created successfully!")
