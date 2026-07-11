# Databricks notebook source
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

accounts_df.write.format("delta").mode("overwrite").saveAsTable("bronze_accounts")
transactions_df.write.format("delta").mode("overwrite").saveAsTable("bronze_transactions")
watchlist_df.write.format("delta").mode("overwrite").saveAsTable("bronze_watchlist")

# COMMAND ----------

from pyspark.sql.functions import col, to_date, trim

# ---- Clean accounts table ----
accounts_clean = spark.table("bronze_accounts") \
    .dropna(subset=["account_id"]) \
    .withColumn("opening_date", to_date(col("opening_date"))) \
    .withColumn("credit_limit", col("credit_limit").cast("double")) \
    .withColumn("customer_name", trim(col("customer_name")))

# credit_limit ke nulls ko 0 se fill karo (ya average se, tumhari choice)
accounts_clean = accounts_clean.fillna({"credit_limit": 0})

# ---- Clean transactions table ----
transactions_clean = spark.table("bronze_transactions") \
    .dropna(subset=["txn_id", "account_id"]) \
    .withColumn("txn_date", to_date(col("txn_date"))) \
    .withColumn("amount", col("amount").cast("double"))

# merchant ke nulls ko "Unknown" se fill karo
transactions_clean = transactions_clean.fillna({"merchant": "Unknown"})

# ---- Join transactions with accounts (enrichment) ----
silver_df = transactions_clean.join(accounts_clean, on="account_id", how="left")

silver_df.show(5)
print("Total rows:", silver_df.count())

# COMMAND ----------

silver_df.write.format("delta").mode("overwrite").saveAsTable("silver_transactions_enriched")

# COMMAND ----------

from pyspark.sql.functions import when, col

# Watchlist se sirf account_id lo aur rename karo taaki join mein confusion na ho
watchlist_clean = spark.table("bronze_watchlist") \
    .dropna(subset=["account_id"]) \
    .select(col("account_id").alias("flagged_account"), "fraud_type", "flagged_date")

# Silver table ko watchlist ke saath left join karo
gold_df = silver_df.join(
    watchlist_clean,
    silver_df.account_id == watchlist_clean.flagged_account,
    how="left"
)

# Agar flagged_account match hua (null nahi hai), toh "fraud" mark karo, warna "normal"
gold_df = gold_df.withColumn(
    "fraud_status",
    when(col("flagged_account").isNotNull(), "fraud").otherwise("normal")
)

gold_df.show(10)
print("Total transactions:", gold_df.count())
print("Fraud transactions:", gold_df.filter(col("fraud_status") == "fraud").count())

# COMMAND ----------

gold_df.write.format("delta").mode("overwrite").saveAsTable("gold_fraud_transactions")

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

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold_fraud_summary
# MAGIC