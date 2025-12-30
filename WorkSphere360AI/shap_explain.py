import shap

def explain_model(model, X_sample):
    explainer = shap.Explainer(model)
    shap_values = explainer(X_sample)

    return shap_values
