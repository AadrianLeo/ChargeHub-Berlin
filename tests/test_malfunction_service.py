import unittest
from unittest.mock import patch
import pandas as pd
import os

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from charging.application.services.malfunction_report_service import MalfunctionService


class TestMalfunctionService(unittest.TestCase):

    def setUp(self):
        # Ensure the directory exists before running the tests
        os.makedirs('./charging/infrastructure/repositories', exist_ok=True)
        
        # Initial DataFrame for testing
        data = {
            'station_name': ['Station A', 'Station B'],
            'report_description': ['Report 1', 'Report 2'],
            'address': ['Address 1', 'Address 2']
        }
        self.reports_df = pd.DataFrame(data)
        self.service = MalfunctionService(self.reports_df)

    def test_initialization(self):
        # Test if the MalfunctionService is initialized with the correct DataFrame
        self.assertEqual(len(self.service.reports_df), 2)
        self.assertIn('station_name', self.service.reports_df.columns)
        self.assertIn('report_description', self.service.reports_df.columns)
        self.assertIn('address', self.service.reports_df.columns)

    def test_add_malfunction_report(self):
        # Test if a malfunction report is correctly added
        new_station_name = 'Station C'
        new_description = 'Report 3'
        new_address = 'Address 3'
        
        updated_df = self.service.add_malfunction_report(new_station_name, new_description, new_address)
        
        # Check if the new report is added
        self.assertEqual(len(updated_df), 3)
        self.assertEqual(updated_df.iloc[2]['station_name'], new_station_name)
        self.assertEqual(updated_df.iloc[2]['report_description'], new_description)
        self.assertEqual(updated_df.iloc[2]['address'], new_address)

    @patch('pandas.DataFrame.to_csv')  # Correct patching of pandas' to_csv function
    def test_add_malfunction_report_csv_save(self, mock_to_csv):
        # Test if the malfunction report is saved to CSV
        new_station_name = 'Station D'
        new_description = 'Report 4'
        new_address = 'Address 4'
        
        # Call the function that writes to CSV
        self.service.add_malfunction_report(new_station_name, new_description, new_address)
        
        # Check if to_csv was called once with the correct arguments
        mock_to_csv.assert_called_once_with('./charging/infrastructure/repositories/malfunction_reports.csv', sep=';', index=False)

    def tearDown(self):
        # Cleanup if necessary (e.g., delete files or reset attributes)
        pass

if __name__ == '__main__':
    unittest.main()
