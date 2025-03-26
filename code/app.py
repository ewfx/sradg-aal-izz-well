import streamlit as st
import pandas as pd
import io
from src.anomaly_detector import detect_anomalies
from src.data_loader import load_data
from src.Catalyst_vs_impact import analyze_catalyst_vs_impact

def main():
    st.warning(
    "⚠️ If you encounter errors while running the analysis, please ensure that you have accepted the model terms at: "
    "[Groq Model Terms](https://console.groq.com/playground?model=mistral-saba-24b).")

    st.title("Data Analysis System")
    
    # Select dataset type
    dataset_type = st.sidebar.selectbox("Select Dataset Type", ["GL & IHUB Data", "Impact & Catalyst Data"])
    
    st.sidebar.header("Upload Files")
    
    if dataset_type == "GL & IHUB Data":
        historical_file = st.sidebar.file_uploader("Upload Historical Data", type=["csv", "xlsx"])
        test_file = st.sidebar.file_uploader("Upload Test Data", type=["csv", "xlsx"])
        
        if historical_file and test_file:
            historical_df, test_df = load_data(historical_file, test_file)
            
            # Clean column names
            historical_df.columns = historical_df.columns.str.strip().str.lower()
            test_df.columns = test_df.columns.str.strip().str.lower()
            
            # Convert 'as of date' column to datetime format
            historical_df['as of date'] = pd.to_datetime(historical_df['as of date'], format="%m/%d/%Y", errors='coerce')
            
            # Sort by 'as of date' in increasing order
            historical_df = historical_df.sort_values(by="as of date", ascending=True)

            st.write("### Preview of Historical Data")
            st.dataframe(historical_df.head())
            st.write("### Preview of Test Data")
            st.dataframe(test_df.head())
            
            if st.button("Run Analysis"):
                required_columns = {"company", "account", "au", "currency", "primary account", "as of date"}
                
                if required_columns.issubset(test_df.columns):
                    results_df = detect_anomalies(historical_df, test_df)
                    merge_keys = ["company", "account", "au", "currency", "primary account", "as of date"]
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
    
    elif dataset_type == "Impact & Catalyst Data":
        file = st.sidebar.file_uploader("Upload Impact & Catalyst Data", type=["csv","xlsx"])
        
        if file:
            df = pd.read_csv(file)
            st.write("### Preview of Uploaded Data")
            st.dataframe(df.head())
            
            if st.button("Run Analysis"):
                result_df = analyze_catalyst_vs_impact(df)
                
                st.write("### Results")
                st.dataframe(result_df.head())
                
                # Convert to XLSX
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    result_df.to_excel(writer, index=False, sheet_name="Results")
                xlsx_data = output.getvalue()
                
                st.download_button(
                    label="Download Results (XLSX)",
                    data=xlsx_data,
                    file_name="catalyst_vs_impact_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

if __name__ == "__main__":
    main()


# import streamlit as st
# import pandas as pd
# import io
# from src.anomaly_detector import detect_anomalies
# from src.data_loader import load_data

# def main():
#     st.title("Anomaly Detection System")
    
#     st.sidebar.header("Upload Files")
#     historical_file = st.sidebar.file_uploader("Upload Historical Data", type=["csv", "xlsx"])
#     test_file = st.sidebar.file_uploader("Upload Test Data", type=["csv", "xlsx"])
    
#     if historical_file and test_file:
#         historical_df, test_df = load_data(historical_file, test_file)
        
#         # Clean column names
#         historical_df.columns = historical_df.columns.str.strip().str.lower()
#         test_df.columns = test_df.columns.str.strip().str.lower()
        
#         st.write("### Preview of Historical Data")
#         st.dataframe(historical_df.head())
#         st.write("### Preview of Test Data")
#         st.dataframe(test_df.head())
        
#         if st.button("Run Anomaly Detection"):
#             # Debugging: Display column names
#             st.write("Test Data Columns:", test_df.columns.tolist())
#             st.write("Train Data Columns:", historical_df.columns.tolist())
#             required_columns = {"company","account","au","currency","primary account", "as of date"}
#             if required_columns.issubset(test_df.columns):
#                 results_df = detect_anomalies(historical_df, test_df)
                
#                 # # Drop 'next steps' column if it exists in results_df
#                 # if "next steps" in results_df.columns:
#                 #     results_df = results_df.drop(columns=["next steps"])
                
#                 merge_keys = ["company","account","au","currency","primary account","as of date"]
#                 final_df = test_df.merge(results_df, on=merge_keys, how="left")
                
#                 st.write("### Results")
#                 st.dataframe(final_df.head())
                
#                 # Convert to XLSX
#                 output = io.BytesIO()
#                 with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#                     final_df.to_excel(writer, index=False, sheet_name="Results")
#                 xlsx_data = output.getvalue()
                
#                 st.download_button(
#                     label="Download Results (XLSX)",
#                     data=xlsx_data,
#                     file_name="anomaly_detection_results.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                 )
#             else:
#                 st.error(f"Missing required columns: {required_columns - set(test_df.columns)}")

# if __name__ == "__main__":
#     main()
