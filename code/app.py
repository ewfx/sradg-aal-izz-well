import streamlit as st
import pandas as pd
from src.anomaly_detector import detect_anomalies
from src.data_loader import load_data


def main():
    st.title("Anomaly Detection System")
    
    st.sidebar.header("Upload Files")
    historical_file = st.sidebar.file_uploader("Upload Historical CSV", type=["csv"])
    test_file = st.sidebar.file_uploader("Upload Test XLSX", type=["xlsx"])
    
    if historical_file and test_file:
        historical_df, test_df = load_data(historical_file, test_file)
        st.write("### Preview of Historical Data")
        st.dataframe(historical_df.head())
        st.write("### Preview of Test Data")
        st.dataframe(test_df.head())
        
        if st.button("Run Anomaly Detection"):
            results_df = detect_anomalies(historical_df, test_df)
            final_df = test_df.merge(results_df, on=["account", "as of date"], how="left")
            
            st.write("### Results")
            st.dataframe(final_df.head())
            
            csv = final_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results",
                data=csv,
                file_name="anomaly_detection_results.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()