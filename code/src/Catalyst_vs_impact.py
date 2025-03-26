import pandas as pd
import numpy as np
import requests
import json
import requests
import re
from src.config import GROQ_API_KEY

def preprocess_data(df):
    date_cols = ['Trade Date', 'Settlement Date', 'Recon Date',
                 'Catalyst Trade Date', 'Catalyst Settlement Date', 'Catalyst Recon Date',
                 'Impact Trade Date', 'Impact Settlement Date', 'Impact Recon Date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    numeric_cols = ['Price', 'Catalyst Price', 'Impact Price', 'Quantity', 'Catalyst Quantity', 'Impact Quantity']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['price_diff'] = abs(df['Catalyst Price'] - df['Impact Price'])
    df['quantity_diff'] = abs(df['Catalyst Quantity'] - df['Impact Quantity'])
    return df


def rule_based_classification(row):
    if pd.isna(row['Catalyst Price']) or row['Catalyst Price'] == 0:
        return "good_to_go", "Catalyst fields empty/zero -> Backend task."
    if pd.isna(row['Impact Price']) or row['Impact Price'] == 0:
        return "good_to_go", "Impact fields empty/zero -> Network delay."
    if row['price_diff'] < 0.1 and row['quantity_diff'] == 0:
        return "good_to_go", "Minor price difference likely due to rounding."
    if row['quantity_diff'] <= 5 and row['price_diff'] == 0:
        return "good_to_go", "Quantity difference is within acceptable limits." 
    return "ambiguous", "Needs further AI-based analysis."

def query_mistral(prompt):
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-saba-24b",
        "messages": [
            {"role": "system", "content": "You are an expert for financial reconciliation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


def extract_json(response_text):
    match = re.search(r"(\{.*\})", response_text, re.DOTALL)
    return match.group(1) if match else None


def comprehensive_ai_analysis(row):
    # If the row is not ambiguous, just return the rule-based suggestion.
    if row['Initial_Classification'] != "ambiguous":
        return "good to go", " ", " "
    
    
    prompt = f"""
Analyze the following reconciliation break

Transaction details:
- Catalyst Price: {row['Catalyst Price']}, Impact Price: {row['Impact Price']}, Price Diff: {row['price_diff']}.
- Catalyst Quantity: {row['Catalyst Quantity']}, Impact Quantity: {row['Impact Quantity']}, Quantity Diff: {row['quantity_diff']}.
- Catalyst Trade Date: {row['Catalyst Trade Date']}, Impact Trade Date: {row['Impact Trade Date']}.
- Catalyst Settlement Date: {row['Catalyst Settlement Date']}, Impact Settlement Date: {row['Impact Settlement Date']}.
- Catalyst Inventory Code: {row['Catalyst Inventory Code']}, Impact Inventory Code: {row['Impact Inventory Code']}
- Catalyst CUSIP: {row['Catalyst CUSIP']}, Impact CUSIP: {row['Impact CUSIP']}
- Catalyst Buy or Sell: {row['Catalyst Buy or Sell']}, Impact Buy or Sell: {row['Impact Buy or Sell']}
        
return your response as a JSON object with keys:
- "classification": Either "anomaly" if the differences are unusual and require investigation or "good_to_go" if the differences are minor or expected.
- "Reason": If "anomaly", provide a brief explanation of around 20 words, otherwise provide a reason why it is good to go in around 20 words.
- "root_cause": If "anomaly", provide the most likely root cause (max 20 words), otherwise " ".

Do not output any text other than the JSON object.


"""
    response = query_mistral(prompt)
    #print(response)
    if not response or response.strip() == "":
        return "error", "No response from API", "error"
    json_text = extract_json(response)
    #parse the response as JSON.
    try:
        result = json.loads(json_text)
        classification = result.get("classification", "error")
        anomaly_reason = result.get("Reason", "error")
        root_cause = result.get("root_cause", "error")
        return classification, anomaly_reason, root_cause
    except Exception as e:
        return "error", f"JSON parse error: {str(e)}", "error"



def analyze_catalyst_vs_impact(df):
    
    # Preprocess the data
    df = preprocess_data(df)
 
    # Apply rule-based classification
    df[['Initial_Classification', 'Comments']] = df.apply(
        lambda row: pd.Series(rule_based_classification(row)), axis=1
    )

    # Apply AI-based analysis for ambiguous cases
    df[['Final_classification', 'Reason', 'root_cause']] = df.apply(
        comprehensive_ai_analysis, axis=1, result_type="expand"
    )
    
    # Save results
    output_path = "reconciliation_analysis_results.csv"
    df.to_csv(output_path, index=False)
    
    return df
    
