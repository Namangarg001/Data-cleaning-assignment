# Fraud Detection Pipeline using PySpark & Databricks (Medallion Architecture)

## 📌 Overview
This project implements a scalable data pipeline to detect fraudulent transactions using **PySpark**, **Spark SQL**, and **Databricks**. The pipeline follows the **Medallion Architecture** (Bronze → Silver → Gold) to progressively clean, enrich, and analyze transaction data, ultimately classifying transactions as `fraud` or `normal` based on a fraud watchlist.

## 🏗️ Architecture