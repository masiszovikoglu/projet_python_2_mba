"""
Tests to improve coverage from 83% to 85%.
Focus on error handlers and edge cases that are actually untested.
"""
import pytest
from src.banking_api.data_manager import DataManager
import pandas as pd


class TestDataManagerErrorHandling:
    """Tests for DataManager error handling and edge cases."""

    def test_load_data_file_not_found(self):
        """Test load_data with non-existent file."""
        manager = DataManager()
        with pytest.raises(FileNotFoundError) as excinfo:
            manager.load_data("nonexistent_file.csv")
        assert "Data file not found" in str(excinfo.value)

    def test_load_data_invalid_csv(self, tmp_path):
        """Test load_data with invalid CSV - missing required columns."""
        # Create invalid CSV without 'id' column
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("wrong,columns\n1,2", encoding="utf-8")
        
        manager = DataManager()
        with pytest.raises(ValueError) as excinfo:
            manager.load_data(str(invalid_csv))
        assert "Error loading data" in str(excinfo.value)

    def test_load_data_with_zip_conversion(self, tmp_path):
        """Test zip field conversion to int and NaN handling."""
        csv_content = """id,amount,zip,card_number,date,year,month,day
1,100.50,75001,1234567890123456,2023-01-15,2023,1,15
2,200.75,,9876543210987654,2023-01-16,2023,1,16"""
        
        csv_file = tmp_path / "test_zip.csv"
        csv_file.write_text(csv_content, encoding="utf-8")
        
        manager = DataManager()
        manager.load_data(str(csv_file))
        
        # Verify zip was converted and NaN filled with 0
        data = manager.get_data()
        assert data.loc[0, "zip"] == 75001
        assert data.loc[1, "zip"] == 0

    def test_load_data_with_text_fields_cleaning(self, tmp_path):
        """Test text fields NaN replacement."""
        csv_content = """id,amount,use_chip,merchant_city,merchant_state,card_number,date,year,month,day
1,100.50,Swipe,Dallas,TX,1234567890123456,2023-01-15,2023,1,15
2,200.75,Online,,CA,9876543210987654,2023-01-16,2023,1,16"""
        
        csv_file = tmp_path / "test_text.csv"
        csv_file.write_text(csv_content, encoding="utf-8")
        
        manager = DataManager()
        manager.load_data(str(csv_file))
        
        # Verify text fields with NaN are replaced with empty string
        data = manager.get_data()
        assert data.loc[1, "merchant_city"] == ""

    def test_load_data_with_errors_field_cleaning(self, tmp_path):
        """Test errors field NaN and 'nan' string handling."""
        csv_content = """id,amount,errors,card_number,date,year,month,day
1,100.50,Bad PIN,1234567890123456,2023-01-15,2023,1,15
2,200.75,,9876543210987654,2023-01-16,2023,1,16
3,50.25,nan,1111222233334444,2023-01-17,2023,1,17"""
        
        csv_file = tmp_path / "test_errors.csv"
        csv_file.write_text(csv_content, encoding="utf-8")
        
        manager = DataManager()
        manager.load_data(str(csv_file))
        
        # Verify errors field handling
        data = manager.get_data()
        assert data.loc[0, "errors"] == "Bad PIN"
        # NaN should become empty string or None
        assert data.loc[1, "errors"] in ["", None, ""]
