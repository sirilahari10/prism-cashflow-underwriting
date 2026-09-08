In credit risk, building the final predictive model is the easy part. The real bottleneck in cash flow underwriting is the data engineering—taking raw, garbled bank transaction memos (like `POS DEBIT 12/04 UBER *EATS 800-555-1212 CA`) and turning them into trustworthy financial features.

I built this Proof of Work to focus on the dirty work. 

Instead of starting with a perfectly clean dataset, this pipeline simulates the ingestion of raw, consumer-permissioned bank data (Open Banking) and processes it into explainable risk attributes.

## How to Run It:
Generate the mess:** Run `generate_mock_transactions.py` to create a dataset of realistic, garbled bank transactions. The PySpark Categorizer (`pyspark/transaction_categorizer.py`):** Uses PySpark to clean, normalize, and categorize raw memo strings into logical buckets (Recurring Income, Housing, BNPL Debt, NSF Fees). The Feature Engine (`sql/cash_flow_features.sql`):** Uses dbt/SQL window functions to build the actual underwriting attributes (30-day spend velocity, free-cash-flow margin, and overdraft flags).
