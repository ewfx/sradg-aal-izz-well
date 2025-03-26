import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from src.models import linear_model, sin_model, quadratic_model, log_model
from src.llm_handler import query_llm

def generate_anomaly_reason(balance_diffs, anomaly, detected_pattern):
    if anomaly == "Yes":
        if max(balance_diffs) - min(balance_diffs) > 10000:
            return "Huge spike in balance detected"
        elif np.std(balance_diffs) > 500:
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
    
    for _, test_row in test_df.iterrows():

        # historical_group = historical_df[historical_df["au"] == au]
        historical_group = historical_df[
            (historical_df["company"] == test_row["company"]) &
            (historical_df["account"] == test_row["account"]) &
            (historical_df["au"] == test_row["au"]) &
            (historical_df["currency"] == test_row["currency"]) &
            (historical_df["primary account"] == test_row["primary account"])
        ]
        
        if historical_group.empty:
            results.append({
                "company":test_row["company"],
                "au": test_row["au"],
                "account":test_row["account"],
                "currency": test_row["currency"],
                "primary account": test_row["primary account"],
                "as of date": test_row["as of date"],
                "Comments": "No historical data available",
                "anomaly": "Yes",
                "next steps": "Review account history"
            })
            continue

        
        
        combined_data = pd.concat([test_row.to_frame().T,historical_group], ignore_index=True).drop_duplicates()
        balance_diffs = combined_data["balance difference"].values
        x_vals = np.arange(len(balance_diffs))
        
        patterns = {
            "Linear": (linear_model, None),
            "Sinusoidal": (sin_model, 10000),
            "Quadratic": (quadratic_model, 10000),
            "Logarithmic": (log_model, None)
        }
        
        detected_pattern = ""
        anomaly = "Yes"
        
        if np.all(np.abs(balance_diffs) < tolerance):
            detected_pattern = "All balance differences are within the threshold"
            anomaly = "No"
        else:
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
        
        results.append({
            "company":test_row["company"],
            "au": test_row["au"],
            "account":test_row["account"],
            "currency": test_row["currency"],
            "primary account": test_row["primary account"],
            "as of date": test_row["as of date"],
            "Comments": anomaly_reason,
            "anomaly": anomaly,
            "next steps": next_steps
        })
    
    return pd.DataFrame(results)
