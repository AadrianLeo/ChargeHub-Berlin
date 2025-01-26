import unittest
from unittest.mock import patch
import pandas as pd
import os
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from charging.application.services.suggestions_service import SuggestionService

class TestSuggestionService(unittest.TestCase):

    def setUp(self):
        # Ensure the directory exists before running the tests
        os.makedirs('./charging/infrastructure/repositories', exist_ok=True)

        # Initial DataFrame for testing
        data = {
            'postal_code': ['12345', '67890'],
            'address': ['Address 1', 'Address 2'],
            'comments': ['Good location', 'Needs better accessibility']
        }
        self.suggestions_df = pd.DataFrame(data)
        self.service = SuggestionService(self.suggestions_df)

    def test_initialization(self):
        # Test if the SuggestionService is initialized with the correct DataFrame
        self.assertEqual(len(self.service.suggestions_df), 2)
        self.assertIn('postal_code', self.service.suggestions_df.columns)
        self.assertIn('address', self.service.suggestions_df.columns)
        self.assertIn('comments', self.service.suggestions_df.columns)

    def test_add_suggestion(self):
        # Test if a suggestion is correctly added
        new_postal_code = '11223'
        new_address = 'Address 3'
        new_comments = 'Great spot for charging'
        
        updated_df = self.service.add_suggestion(new_postal_code, new_address, new_comments)
        
        # Check if the new suggestion is added
        self.assertEqual(len(updated_df), 3)
        self.assertEqual(updated_df.iloc[2]['postal_code'], new_postal_code)
        self.assertEqual(updated_df.iloc[2]['address'], new_address)
        self.assertEqual(updated_df.iloc[2]['comments'], new_comments)

    @patch('pandas.DataFrame.to_csv')  # Correct patching of pandas' to_csv function
    def test_add_suggestion_csv_save(self, mock_to_csv):
        # Test if the suggestion is saved to CSV
        new_postal_code = '33445'
        new_address = 'Address 4'
        new_comments = 'Location near a mall'
        
        # Call the function that writes to CSV
        self.service.add_suggestion(new_postal_code, new_address, new_comments)
        
        # Check if to_csv was called once with the correct arguments
        mock_to_csv.assert_called_once_with('./charging/infrastructure/repositories/suggestions.csv', sep=';', index=False)

    def tearDown(self):
        # Cleanup if necessary (e.g., delete files or reset attributes)
        pass

if __name__ == '__main__':
    unittest.main()
