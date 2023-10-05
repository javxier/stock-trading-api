import unittest
from unittest.mock import patch
from io import StringIO
import os
import pandas as pd
from MVCstockDownloader import *

class TestStockDataAnalysis(unittest.TestCase):
    def test_calculate_moving_average_signals(self):
        try:
            calculate_moving_average_signals('FNGD_stock_data.json')
        except Exception as e:
            self.fail(f"calculate_moving_average_signals raised exception {e}")

    def test_bollinger_bands_strategy(self):
        try:
            bollinger_bands_strategy('FNGD_stock_data.json')
        except Exception as e:
            self.fail(f"bollinger_bands_strategy raised exception {e}")

    @patch('builtins.input', return_value='FNGU')
    @patch('builtins.print')
    def test_stockdatamodel_set_data(self, mock_print, mock_input):
        model = StockDataModel()
        model.set_data('FNGU', '2020-01-01', '2020-12-31')
        self.assertEqual(model.symbol, 'FNGU')
        self.assertEqual(model.start_date, '2020-01-01')
        self.assertEqual(model.end_date, '2020-12-31')

    @patch('builtins.input', return_value='FNGU')
    @patch('builtins.print')
    def test_stockdatamodel_save_load_json(self, mock_print, mock_input):
        model = StockDataModel()
        model.set_data('FNGU', '2020-01-01', '2020-12-31')
        data = {
            "2020-01-01": {
                "open": "1",
                "high": "2",
                "low": "1",
                "close": "2",
                "volume": "1000"
            },
            "2020-01-02": {
                "open": "2",
                "high": "3",
                "low": "2",
                "close": "3",
                "volume": "2000"
            }
        }
        model.save_data_as_json(data, 'test_save.json')
        loaded_data = model.load_data_from_json('test_save.json')
        self.assertEqual(data, loaded_data)
        if os.path.exists('test_save.json'):
            os.remove('test_save.json')

    @patch('builtins.input', return_value='FNGU')
    @patch('builtins.print')
    def test_stockdataview_display_data(self, mock_print, mock_input):
        view = StockDataView()
        data = {
            "2020-01-01": {
                "open": "1",
                "high": "2",
                "low": "1",
                "close": "2",
                "volume": "1000"
            },
            "2020-01-02": {
                "open": "2",
                "high": "3",
                "low": "2",
                "close": "3",
                "volume": "2000"
            }
        }
        view.display_data(data)
        mock_print.assert_called()



if __name__ == '__main__':
    unittest.main()
