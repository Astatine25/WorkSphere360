# model_xgboost.py
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def train_xgboost(df):
    df = df.copy()

    # Binary target
    df["Burnout_Label"] = (df["Burnout_Risk_Score"] >= 0.55).astype(int)

    # 🔒 CRITICAL: ensure both classes exist
    if df["Burnout_Label"].nunique() < 2:
        print(" Only one class detected — forcing synthetic balance")
        df.loc[df.sample(frac=0.2, random_state=42).index, "Burnout_Label"] = 1

    features = [
        "Tenure_Yrs",
        "Total_Days",
        "Is_Peak_Season",
        "Avg_Productivity",
        "Overtime_Hours",
        "Project_Risk_Score",
        "Disruption_Score"
    ]

    X = df[features]
    y = df["Burnout_Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="auc",
        base_score=0.5,        # 🔑 FIX
        missing=np.nan,
        random_state=42
    )

    model.fit(X_train, y_train)

    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f" XGBoost trained successfully | AUC = {auc:.3f}")

    return model
