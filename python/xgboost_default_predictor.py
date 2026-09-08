"""
Takes the structured features from the dbt output and trains a baseline 
Gradient Boosting model to predict loan default probability.
"""
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# In production, this would load the output of cash_flow_features.sql
# df = pd.read_parquet("s3://processed-zone/underwriting_features/")

def train_baseline_model(df):
    # Define our engineered features
    features = ['monthly_recurring_income', 'monthly_fixed_expenses', 'nsf_count_30d', 'estimated_free_cash_flow']
    X = df[features]
    y = df['default_flag'] # Historical target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a baseline XGBoost model
    clf = XGBClassifier(eval_metric='logloss')
    clf.fit(X_train, y_train)

    # Evaluate performance
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.3f}")
    print(classification_report(y_test, y_pred))
    
    # Returning feature importances (NSF count is usually the strongest predictor)
    return clf.feature_importances_
