-- dbt Model: Cash Flow Feature Engineering for Underwriting
-- Calculates recurring income stability and overdraft risk from categorized transactions

{{ config(materialized='table', tags=['cash_flow_features']) }}

WITH categorized_tx AS (
    SELECT * FROM {{ ref('stg_categorized_transactions') }}
),

inflow_outflow_metrics AS (
    SELECT 
        account_id,
        DATE_TRUNC('month', transaction_date) AS tx_month,
        
        -- Feature 1: Recurring Income Detection
        SUM(IFF(tx_category = 'Income' AND amount > 0, amount, 0)) AS monthly_recurring_income,
        
        -- Feature 2: Non-Discretionary Spend (Rent, Utilities)
        SUM(IFF(tx_category IN ('Housing', 'Utilities'), ABS(amount), 0)) AS monthly_fixed_expenses,
        
        -- Feature 3: Overdraft / NSF Risk Flags (Highly predictive of default)
        COUNT(IFF(tx_category = 'Overdraft_Fee', 1, NULL)) AS nsf_count_30d
        
    FROM categorized_tx
    GROUP BY account_id, DATE_TRUNC('month', transaction_date)
)

SELECT 
    account_id,
    tx_month,
    monthly_recurring_income,
    monthly_fixed_expenses,
    nsf_count_30d,
    
    -- Feature 4: Free Cash Flow Margin (Income vs Fixed Expenses)
    (monthly_recurring_income - monthly_fixed_expenses) AS estimated_free_cash_flow,
    
    -- Flag highly stressed accounts (living paycheck-to-paycheck with overdrafts)
    IFF((monthly_recurring_income - monthly_fixed_expenses < 200) AND nsf_count_30d > 0, TRUE, FALSE) as is_high_risk_cashflow
FROM inflow_outflow_metrics;
