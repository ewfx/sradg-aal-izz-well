import pandas as pd

def load_data(historical_file, test_file):
    # Determine file type and read accordingly
    def read_file(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        elif file.name.endswith((".xls", ".xlsx")):
            return pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV or XLSX files.")

    historical_df = read_file(historical_file)
    test_df = read_file(test_file)

    # Convert column names to lowercase
    historical_df.columns = historical_df.columns.str.lower()
    test_df.columns = test_df.columns.str.lower()

    # Compute balance difference
    historical_df["balance difference"] = historical_df["gl balance"] - historical_df["ihub balance"]
    test_df["balance difference"] = test_df["gl balance"] - test_df["ihub balance"]

    return historical_df, test_df
