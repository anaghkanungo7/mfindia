import unittest
from datetime import datetime
from mfindia.main import getMarketSnapshot
import pandas as pd

class TestGetSnapshot(unittest.TestCase):

    def test_getSnapshot(self):
        date = datetime(2023, 1, 1)
        df = getMarketSnapshot(date)
        
        # Assert that the returned object is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Assert that the DataFrame is not empty
        self.assertTrue(df.empty == False)

        # Check the column names
        # After renaming 'Net Asset Value' to 'ticker_close' and 'Date\r' to 'Date'
        expected_columns = ['Scheme Code', 'Scheme Name', 'ISIN Div Payout/ISIN Growth', 'ISIN Div Reinvestment', 'ticker_close', 'Repurchase Price', 'Sale Price', 'Date']
        self.assertEqual(df.columns.tolist(), expected_columns)

if __name__ == '__main__':
    unittest.main()
