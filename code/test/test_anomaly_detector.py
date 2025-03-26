import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.anomaly_detector import detect_anomalies

@pytest.fixture
def mock_data():
    """Fixture for creating mock historical and test data."""
    historical_data = pd.DataFrame({
        "account": ["A1", "A2", "A3"],
        "as of date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "balance difference": [100, 200, -150]
    })

    test_data = pd.DataFrame({
        "account": ["A1", "A2", "A3"],
        "as of date": ["2024-01-04", "2024-01-05", "2024-01-06"],
        "balance difference": [110, 220, -140]
    })

    return historical_data, test_data

def test_detect_anomalies(mock_data):
    """Test anomaly detection function."""
    historical_data, test_data = mock_data
    results = detect_anomalies(historical_data, test_data)

    assert not results.empty, "Results should not be empty"
    assert "account" in results.columns, "Account column missing in results"
    assert "anomaly" in results.columns, "Anomaly column missing in results"
    assert "Comment" in results.columns, "Comment column missing in results"
    assert isinstance(results, pd.DataFrame), "Result should be a pandas DataFrame"
