import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from src.models import linear_model, sin_model, quadratic_model, log_model
from src.llm_handler import query_llm

def generate_anomaly_reason(balance_diffs, anomaly, detected_pattern):
    if anomaly == "Yes":
        if max(balance_diffs) - min(balance_diffs) > 5000:
            return "Huge spike in balance detected"
        elif np.std(balance_diffs) > 1000:
            return "Inconsistent variation in balance detected"
        else:
            prompt = f"Analyze balance history and provide the reason behind the anomaly. Using: {balance_diffs}. IN 8-10 WORDS CRISP AND CLEAR"
            return query_llm(prompt)
    else:
        return detected_pattern

def generate_next_steps(balance_diffs, anomaly):
    prompt = f"Analyze balance history and provide next steps. Anomaly detected: {anomaly}. IN 8-10 WORDS CRISP AND CLEAR"
    return query_llm(prompt) if anomaly == "Yes" else "No action needed"

def detect_anomalies(historical_df, test_df):
    results = []
    tolerance = 1
    
    for index, test_row in test_df.iterrows():
        account = test_row["account"]
        balance_diff = test_row["balance difference"]
        historical_group = historical_df[historical_df["account"] == account]
        
        if historical_group.empty:
            results.append({"account": account, "as of date": test_row["as of date"], "Comment": "No historical data available", "anomaly": "Yes", "next steps": "Review account history"})
            continue
        
        balance_diffs = np.concatenate([historical_group["balance difference"].values, [balance_diff]])
        x_vals = np.arange(len(balance_diffs))
        
        patterns = {
            "Linear": (linear_model, None),
            "Sinusoidal": (sin_model, 10000),
            "Quadratic": (quadratic_model, 10000),
            "Logarithmic": (log_model, None)
        }
        
        detected_pattern = ""
        anomaly = "Yes"
        
        try:
            popt, _ = curve_fit(linear_model, x_vals, balance_diffs)
            fit_values = linear_model(x_vals, *popt)
            residuals = np.abs(balance_diffs - fit_values)
            if np.all(residuals < tolerance):
                detected_pattern = "Linear pattern observed"
                anomaly = "No"
        except:
            pass
        
        if anomaly == "Yes":
            for pattern_name, (model, maxfev) in patterns.items():
                if pattern_name == "Linear":
                    continue
                try:
                    popt, _ = curve_fit(model, x_vals, balance_diffs, maxfev=maxfev)
                    fit_values = model(x_vals, *popt)
                    residuals = np.abs(balance_diffs - fit_values)
                    if np.all(residuals < tolerance):
                        detected_pattern = f"{pattern_name} pattern observed"
                        anomaly = "No"
                        break
                except:
                    continue
        
        anomaly_reason = generate_anomaly_reason(balance_diffs, anomaly, detected_pattern)
        next_steps = generate_next_steps(balance_diffs, anomaly)
        results.append({"account": account, "as of date": test_row["as of date"], "Comment": anomaly_reason, "anomaly": anomaly, "next steps": next_steps})
    
    return pd.DataFrame(results)
