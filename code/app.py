import streamlit as st
import pandas as pd
import io
from src.anomaly_detector import detect_anomalies
from src.data_loader import load_data

def main():
    st.title("Anomaly Detection System")
    
    st.sidebar.header("Upload Files")
    historical_file = st.sidebar.file_uploader("Upload Historical Data", type=["csv", "xlsx"])
    test_file = st.sidebar.file_uploader("Upload Test Data", type=["csv", "xlsx"])
    
    if historical_file and test_file:
        historical_df, test_df = load_data(historical_file, test_file)
        
        # Clean column names
        historical_df.columns = historical_df.columns.str.strip().str.lower()
        test_df.columns = test_df.columns.str.strip().str.lower()
        
        st.write("### Preview of Historical Data")
        st.dataframe(historical_df.head())
        st.write("### Preview of Test Data")
        st.dataframe(test_df.head())
        
        if st.button("Run Anomaly Detection"):
            # Debugging: Display column names
            st.write("Test Data Columns:", test_df.columns.tolist())
            st.write("Train Data Columns:", historical_df.columns.tolist())
            required_columns = {"company","account","au","currency","primary account", "as of date"}
            if required_columns.issubset(test_df.columns):
                results_df = detect_anomalies(historical_df, test_df)
                
                # # Drop 'next steps' column if it exists in results_df
                # if "next steps" in results_df.columns:
                #     results_df = results_df.drop(columns=["next steps"])
                
                merge_keys = ["company","account","au","currency","primary account","as of date"]
                final_df = test_df.merge(results_df, on=merge_keys, how="left")
                
                st.write("### Results")
                st.dataframe(final_df.head())
                
                # Convert to XLSX
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    final_df.to_excel(writer, index=False, sheet_name="Results")
                xlsx_data = output.getvalue()
                
                st.download_button(
                    label="Download Results (XLSX)",
                    data=xlsx_data,
                    file_name="anomaly_detection_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(f"Missing required columns: {required_columns - set(test_df.columns)}")

if __name__ == "__main__":
    main()
