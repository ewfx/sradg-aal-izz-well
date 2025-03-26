import pytest
import pandas as pd
from io import StringIO, BytesIO
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_loader import load_data

@pytest.fixture
def mock_csv_data():
    """Simulates an uploaded CSV file for historical data."""
    csv_content = """account,as of date,gl balance,ihub balance
A1,2024-01-01,1000,1000
A2,2024-01-02,200,250
A3,2024-01-03,400,250"""
    return StringIO(csv_content)

@pytest.fixture
def mock_xlsx_data():
    """Simulates an uploaded XLSX file for test data."""
    xlsx_data = BytesIO()
    df = pd.DataFrame({
        "account": ["A1", "A2", "A3"],
        "as of date": ["2024-01-04", "2024-01-05", "2024-01-06"],
        "gl balance": [110, 220, 140],
        "ihub balance": [210, 320, 140]
    })
    with pd.ExcelWriter(xlsx_data, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    xlsx_data.seek(0)  # Reset buffer position
    return xlsx_data

def test_load_data(mock_csv_data, mock_xlsx_data):
    """Test if load_data correctly loads CSV and XLSX files."""
    historical_df, test_df = load_data(mock_csv_data, mock_xlsx_data)

    # Check DataFrame types
    assert isinstance(historical_df, pd.DataFrame), "Historical data should be a DataFrame"
    assert isinstance(test_df, pd.DataFrame), "Test data should be a DataFrame"

    # Validate columns exist
    expected_columns = {"account", "as of date", "balance difference"}
    assert expected_columns.issubset(historical_df.columns), "Historical data missing expected columns"
    assert expected_columns.issubset(test_df.columns), "Test data missing expected columns"

    # Check data integrity
    assert len(historical_df) == 3, "Historical data should have 3 rows"
    assert len(test_df) == 3, "Test data should have 3 rows"
    assert test_df.iloc[0]["account"] == "A1", "First account in test data should be A1"
