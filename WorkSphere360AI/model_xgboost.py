import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

FEATURES = [
    "Tenure",
    "Bradford_Factor",
    "Overtime_Hours_Last_30_Days",
    "Days_Since_Last_Vacation",
    "Average_Productivity_Score",
    "Burnout_Risk_Score"
]

def train_xgboost(df):
    X = df[FEATURES]
    y = (df["Burnout_Risk_Score"] > 0.65).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="auc"
    )

    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)

    print(f"Model AUC: {auc:.3f}")

    return model
V
