"""
Generates messy, unstructured bank transaction data to test the PySpark categorizer.
Run this script to create 'raw_transactions.csv'.
"""
import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

def create_messy_data():
    np.random.seed(42)
    now = datetime.utcnow()
    
    # Simulating the garbage strings you actually get from bank APIs
    messy_memos = [
        ("ACH DEBIT - UBER *EATS 800-555-1212 CA", -35.50),
        ("DIR DEP PAYROLL - ACME CORP PPD ID 987654321", 2450.00),
        ("RETURNED ITEM FEE - INSUFFICIENT FUNDS", -35.00),
        ("KLARNA * PAY IN 4 WEB PMT", -45.25),
        ("POS PUR CVS/PHARMACY #1234 TX", -12.99),
        ("ONLINE TRANSFER TO APT 4B PROPERTY MGMT", -1500.00),
        ("GIG EARNINGS DOORDASH INC", 112.50)
    ]
    
    data = []
    for _ in range(50):
        memo, amount = messy_memos[np.random.randint(0, len(messy_memos))]
        data.append({
            "transaction_id": str(uuid.uuid4()),
            "account_id": "acc_1001", # Simulating a single user
            "transaction_date": (now - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
            "raw_merchant_string": memo,
            "amount": amount
        })
        
    df = pd.DataFrame(data)
    df.to_csv("raw_transactions.csv", index=False)
    print("Generated 50 messy transactions in raw_transactions.csv")

if __name__ == "__main__":
    create_messy_data()
