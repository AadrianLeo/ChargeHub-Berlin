import unittest
import pandas as pd
from unittest.mock import patch
from charging.application.services.search_service import SearchService

class TestSearchService(unittest.TestCase):
    def setUp(self):
        # Sample dataset for testing
        self.sample_data = {
            "Postleitzahl": [10115, 10115, 10243, 10317],
            "Breitengrad": ["52.5303", "52.5312", "52.5105", "52.4907"],
            "Längengrad": ["13.3846", "13.3857", "13.4415", "13.4684"],
            "Anzeigename (Karte)": ["Station A", "Station B", "Station C", "Station D"],
        }
        self.df_lstat = pd.DataFrame(self.sample_data)
        self.service = SearchService(self.df_lstat)

    def test_initialization(self):
        # Test initialization of SearchService
        self.assertIsNotNone(self.service.df_lstat)
        self.assertEqual(len(self.service.df_lstat), 4)

    def test_search_by_valid_postal_code(self):
        # Test with a postal code that exists
        postal_code = 10115
        result = self.service.search_by_postal_code(postal_code)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Station A")
        self.assertEqual(result[0]["status"], "Available")
        self.assertEqual(result[1]["name"], "Station B")
        self.assertEqual(result[1]["status"], "Available")

    def test_search_by_invalid_postal_code(self):
        # Test with a postal code that doesn't exist
        postal_code = 99999
        result = self.service.search_by_postal_code(postal_code)
        self.assertEqual(len(result), 0)

    def test_search_by_none_postal_code(self):
        # Test with None as a postal code
        result = self.service.search_by_postal_code(None)
        self.assertEqual(len(result), 0)

    def test_search_by_string_postal_code(self):
        # Test with a string postal code
        postal_code = "10115"
        result = self.service.search_by_postal_code(postal_code)
        self.assertEqual(len(result), 2)

    def test_search_by_float_postal_code(self):
        # Test with a float postal code
        postal_code = 10115.0
        result = self.service.search_by_postal_code(postal_code)
        self.assertEqual(len(result), 2)

    def test_postal_code_normalization(self):
        # Test postal code normalization in the dataframe
        self.df_lstat.loc[0, "Postleitzahl"] = float("10115.0")
        self.service.df_lstat = self.df_lstat
        result = self.service.search_by_postal_code(10115)
        self.assertEqual(len(result), 2)

    def test_search_by_mixed_type_postal_codes(self):
        # Test with mixed type postal codes in the dataframe
        self.df_lstat.loc[0, "Postleitzahl"] = "10115.0"
        self.service.df_lstat = self.df_lstat
        result = self.service.search_by_postal_code(10115)
        self.assertEqual(len(result), 2)

    def test_output_format(self):
        # Test the output format of stations
        postal_code = 10115
        result = self.service.search_by_postal_code(postal_code)
        for station in result:
            self.assertIn("name", station)
            self.assertIn("status", station)
            self.assertIn("location", station)
            self.assertIsInstance(station["location"], tuple)
            self.assertIsInstance(station["location"][0], float)
            self.assertIsInstance(station["location"][1], float)

    def test_handling_nan_postal_code(self):
        # Test if NaN postal codes are handled gracefully
        self.df_lstat.loc[0, "Postleitzahl"] = float("nan")
        self.service.df_lstat = self.df_lstat
        result = self.service.search_by_postal_code(10115)
        self.assertEqual(len(result), 1)  # Remaining valid entry

    # Test logging for invalid postal code
    @patch("charging.application.services.search_service.logging")
    def test_invalid_postal_code_logging(self, mock_logging):
        postal_code = "abc123"
        self.service.search_by_postal_code(postal_code)
        mock_logging.warning.assert_called_with(f"Invalid postal code provided: {postal_code}")

    # Test exception handling when unexpected error occurs
    @patch("charging.application.services.search_service.logging")
    def test_unexpected_error_logging(self, mock_logging):
        # Simulate an unexpected error by passing a DataFrame with a broken structure
        self.service.df_lstat = None  # This will cause an AttributeError when accessed
        result = self.service.search_by_postal_code(10115)
        mock_logging.error.assert_called_with("An unexpected error occurred: 'NoneType' object has no attribute 'Postleitzahl'")

if __name__ == "__main__":
    unittest.main()
