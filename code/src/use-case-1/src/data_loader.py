import pandas as pd

def load_data(historical_file, test_file):
    historical_df = pd.read_csv(historical_file)
    test_df = pd.read_excel(test_file)
    historical_df.columns = historical_df.columns.str.lower()
    test_df.columns = test_df.columns.str.lower()
    
    historical_df["balance difference"] = historical_df["gl balance"] - historical_df["ihub balance"]
    test_df["balance difference"] = test_df["gl balance"] - test_df["ihub balance"]
    
    return historical_df, test_df