import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def train_xgboost(df: pd.DataFrame):
    """
    Train XGBoost classifier for Burnout risk
    """

    df = df.copy()

    # Ensure target is exactly 0 or 1
    df["Burnout_Label"] = (df["Burnout_Risk_Score"] > 0.60).astype(int)
    df["Burnout_Label"] = df["Burnout_Label"].clip(0, 1)

    features = [
        "Bradford_Factor",
        "Total_Absence_Days",
        "Absence_Count",
        "Days_Since_Last_Vacation",
        "Overtime_Hours_Last_30_Days",
        "Average_Productivity_Score"
    ]

    X = df[features].replace([np.inf, -np.inf], np.nan).fillna(0)
    y = df["Burnout_Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(
        n_estimators=250,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="auc",
        missing=np.nan,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f" XGBoost Model Trained | AUC: {auc:.3f}")

    return model
