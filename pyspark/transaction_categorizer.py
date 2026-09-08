"""
PySpark Pipeline: Cleans raw, unstructured bank transaction memos and applies 
regex logic to categorize inflows and outflows for credit scoring.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, when, trim, regexp_replace

spark = SparkSession.builder.appName("Prism_CashFlow_Categorizer").getOrCreate()

# Load the messy data
df_raw = spark.read.csv("../raw_transactions.csv", header=True, inferSchema=True)

# Clean the raw merchant strings (remove special characters and trim whitespace)
df_clean = df_raw.withColumn("memo_clean", trim(regexp_replace(lower(col("raw_merchant_string")), "[^a-zA-Z0-9 ]", "")))

# Heuristic-based Categorization (Feature engineering baseline for downstream models)
df_categorized = df_clean.withColumn(
    "tx_category",
    when(col("memo_clean").rlike("payroll|dir dep|salary|gig earnings|doordash"), "Income")
    .when(col("memo_clean").rlike("apt|rent|mortgage|property mgmt"), "Housing")
    .when(col("memo_clean").rlike("insufficient|nsf|returned item fee"), "Overdraft_Fee")
    .when(col("memo_clean").rlike("affirm|klarna|afterpay"), "BNPL_Debt")
    .otherwise("Discretionary")
)

df_categorized.select("raw_merchant_string", "amount", "tx_category").show(truncate=False)
# In production: df_categorized.write.mode("overwrite").parquet("s3://processed-zone/transactions/")
