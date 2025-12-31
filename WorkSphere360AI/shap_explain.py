# shap_explain.py
import shap
import pandas as pd

def compute_shap_values(model, X_sample):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    return shap_values
