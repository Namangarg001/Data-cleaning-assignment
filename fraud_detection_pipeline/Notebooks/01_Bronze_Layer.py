# Databricks notebook source
# =========================================================
# 01_Bronze_Layer.py
# Purpose: Raw data ingestion (Bronze Layer)
# Reads raw CSV files (accounts, transactions, fraud watchlist)
# and saves them as Delta tables without any transformation.
# =========================================================

# COMMAND ----------

# Update these paths to match your Databricks volume location
accounts_path = "/Volumes/workspace/default/fraud_project/accounts (1).csv"
transactions_path = "/Volumes/workspace/default/fraud_project/transactions.csv"
watchlist_path = "/Volumes/workspace/default/fraud_project/known_fraud_accounts.csv"

accounts_df = spark.read.csv(accounts_path, header=True, inferSchema=True)
transactions_df = spark.read.csv(transactions_path, header=True, inferSchema=True)
watchlist_df = spark.read.csv(watchlist_path, header=True, inferSchema=True)

accounts_df.show(5)
transactions_df.show(5)
watchlist_df.show(5)

# COMMAND ----------

# Save raw data as Bronze Delta tables
accounts_df.write.format("delta").mode("overwrite").saveAsTable("bronze_accounts")
transactions_df.write.format("delta").mode("overwrite").saveAsTable("bronze_transactions")
watchlist_df.write.format("delta").mode("overwrite").saveAsTable("bronze_watchlist")

print("Bronze tables created successfully!")
