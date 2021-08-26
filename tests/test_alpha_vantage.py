import csv
import os
import shutil
import time
import unittest
from typing import Dict, Union

from dateutil.parser import parse

from alpha_vantage.alpha_vantage import AlphaVantage
from constants import DEFAULT_OUTPUT_FOLDER, GRACE_PERIOD
from helpers.custom_exceptions_helper import WrongInputValueException, AlphaVantageApiException


class AlphaVantageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This is run once, when initiating the class
        :return:
        """
        cls._OUTPUT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), DEFAULT_OUTPUT_FOLDER)
        os.mkdir(cls._OUTPUT_PATH)
        cls._API_KEY = 'TEST_API_KEY'
        cls.alpha_vantage = AlphaVantage(key=cls._API_KEY, output_format='csv')

    def test_search_api(self):
        """ Test search api
        There are two cases, one of which is failure due to invalid keyword,
        the second is success of retrieving a list of matched result according to the provided keyword.
        :return:
        """
        # fail case, when keyword is an empty string
        _keyword = ''
        self.assertRaises(AlphaVantageApiException, self.alpha_vantage.search, _keyword)

        # success case
        _keyword = 'ba'
        result = self.alpha_vantage.search(keyword=_keyword)
        self.assertIsInstance(result, list, "The returned search result is not a list.")
        self.assertGreater(len(result), 0, "The returned search result is empty.")
        # check one object in the list
        self.assertIsInstance(result[0], dict, "The items in the search result is not a python dictionary.")
        keys_in_dict = ['1. symbol', '2. name', '3. type', '4. region',
                        '5. marketOpen', '6. marketClose', '7. timezone', '8. currency', '9. matchScore']
        self.assertEqual(len(set(keys_in_dict).union(result[0].keys())), len(keys_in_dict),
                         "The search result did not contain the correct data, the dictionary keys seems inconsistent.")
        return None

    def test_quote_api(self):
        """ Test quote api
        There are two cases, one of which is failure due to invalid symbol,
        the second is success of retrieving a dictionary of rhe current quote for the provided keyword.
        :return:
        """
        # fail case, when symbol is an empty string
        _symbol = ''
        self.assertRaises(AlphaVantageApiException, self.alpha_vantage.get_current_quote, _symbol)

        # success case
        _symbol = 'IBM'
        result = self.alpha_vantage.get_current_quote(symbol=_symbol, force_json=True)
        keys_in_dict = ['01. symbol', '02. open', '03. high', '04. low', '05. price',
                        '06. volume', '07. latest trading day', '08. previous close', '09. change',
                        '10. change percent']
        self.assertIsInstance(result, dict, "The quote result is not a python dictionary.")
        self.assertEqual(len(set(keys_in_dict).union(result.keys())), len(keys_in_dict),
                         "The quote result did not contain the correct data, the dictionary keys seems inconsistent.")
        self.assertEqual(result['01. symbol'], 'IBM',
                         "The quote result did not contain the correct data, the dictionary values seems inconsistent.")
        return None

    def test_ema_api(self):
        """ Test exponential moving average api
        There are three cases, two of which are failure cases due to wrong input,
        the third is success of retrieving a dictionary of the exponential moving average for the provided company.
        :return:
        """
        _symbol = 'IBM'
        _interval = 'daily'
        _time_period = 50

        # first fail case: wrong series type
        _series_type = ''
        self.assertRaises(WrongInputValueException, self.alpha_vantage.get_ema, symbol=_symbol,
                          interval=_interval, time_period=_time_period, series_type=_series_type)
        _series_type = 'low'

        # second fail case: wrong interval
        _interval = ''
        self.assertRaises(WrongInputValueException, self.alpha_vantage.get_ema, symbol=_symbol,
                          interval=_interval, time_period=_time_period, series_type=_series_type)
        _interval = 'daily'

        # success case:
        result = self.alpha_vantage.get_ema(symbol=_symbol, interval=_interval, time_period=_time_period,
                                            series_type=_series_type, force_json=True)
        self.assertIsInstance(result, dict, "The ema result is not a python dictionary.")
        dates_keys = list(result.keys())
        self.assertGreater(len(dates_keys), 0, 'The returned dictionary of EMA function is empty.')
        self.assertTrue(parse(dates_keys[0]), 'The keys in the returned dictionary of EMA function are not correct.')
        self.assertIsInstance(result[dates_keys[0]], dict, "The ema result values are not a python dictionary.")
        self.assertEqual(list(result[dates_keys[0]].keys())[0], 'EMA', "The ema result values does not have `EMA` key.")
        return None

    def test_intraday_timeseries_api(self):
        """ Test intraday api
        There are three cases, one of which is failure case due to wrong input,
        the second and third are success of retrieving a dictionary of the intraday timeseries for the provided company
        either as json or csv.
        :return:
        """
        _symbol = 'IBM'

        # fail case: wrong interval
        _interval = 'wrong_interval'
        self.assertRaises(WrongInputValueException, self.alpha_vantage.get_intraday, symbol=_symbol, interval=_interval,
                          force_json=True)
        _interval = '1min'

        # success case (json):
        result = self.alpha_vantage.get_intraday(symbol=_symbol, interval=_interval, force_json=True)
        self._test_timeseries_result(result=result)

        # success case (csv):
        result = self.alpha_vantage.get_intraday(symbol=_symbol, interval=_interval, force_json=False)
        self._test_timeseries_result(result=result)
        return None

    def test_daily_timeseries_api(self):
        """ Test daily api
        There are two cases, to test the success of retrieving a dictionary of the daily timeseries
        for the provided company either as json or csv.
        """
        _symbol = 'IBM'

        # success case (json):
        result = self.alpha_vantage.get_daily_timeseries(symbol=_symbol, force_json=True)
        self._test_timeseries_result(result=result)

        # success case (csv):
        result = self.alpha_vantage.get_daily_timeseries(symbol=_symbol, force_json=False)
        self._test_timeseries_result(result=result)

        return None

    def test_weekly_timeseries_api(self):
        """ Test daily api
        There are two cases, to test the success of retrieving a dictionary of the weekly timeseries
        for the provided company either as json or csv.
        """
        # so far, 5 requests have been sent in one minute, so we need to wait a minute then continue the tests
        # since the limit of using apis was exceeded (5 requests per minute)
        _symbol = 'IBM'

        # success case (json):
        result = self.alpha_vantage.get_weekly_timeseries(symbol=_symbol, force_json=True)
        self._test_timeseries_result(result=result)

        # success case (csv):
        result = self.alpha_vantage.get_weekly_timeseries(symbol=_symbol, force_json=False)
        self._test_timeseries_result(result=result)

        return None

    def test_monthly_timeseries_api(self):
        """ Test daily api
        There are two cases, to test the success of retrieving a dictionary of the monthly timeseries
        for the provided company either as json or csv.
        """
        _symbol = 'IBM'

        # success case (json):
        result = self.alpha_vantage.get_monthly_timeseries(symbol=_symbol, force_json=True)
        self._test_timeseries_result(result=result)

        # success case (csv):
        result = self.alpha_vantage.get_monthly_timeseries(symbol=_symbol, force_json=False)
        self._test_timeseries_result(result=result)

        return None

    def _test_timeseries_result(self, result: Union[Dict[str, Dict[str, str]], bytes]) -> None:
        """
        Test the result of timeseries api, the result could be a json or bytes, to be saved in csv
        :param result:
        :return:
        """
        if isinstance(result, dict):
            self.assertIsInstance(result, dict, "The result is not a python dictionary.")
            dates_keys = list(result.keys())
            self.assertGreater(len(dates_keys), 0, 'The returned json is empty.')
            self.assertTrue(parse(dates_keys[0]),
                            'The keys in the returned json are not correct, they should be dates.')
            self.assertIsInstance(result[dates_keys[0]], dict, "The result values are not a json object.")
            values_keys = ['1. open', '2. high', '3. low', '4. close', '5. volume']
            result_values_keys = list(result[dates_keys[0]].keys())
            self.assertEqual(len(set(values_keys).union(result_values_keys)), len(values_keys),
                             "The result did not contain the correct data, the json keys seem inconsistent.")

        elif isinstance(result, bytes):
            # take the bytes data, save them in csv file, check if the data saved correctly.
            timestamp = time.time()
            file_name = os.path.join(self._OUTPUT_PATH, f'test_{timestamp}.csv')
            with open(file_name, "wb") as outfile:
                outfile.write(result)
            outfile.close()

            with open(file_name, 'r') as reader_file:
                reader = csv.DictReader(reader_file)
                for line in reader:
                    self.assertIsInstance(line, dict, "The result is not a python dictionary.")
                    dict_keys = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                    self.assertEqual(len(set(dict_keys).union(line.keys())), len(dict_keys),
                                     "The result did not contain the correct data, the json keys seem inconsistent.")
                    self.assertTrue(parse(line['timestamp']), 'The timestamp in the json is not a correct.')
            reader_file.close()

    def tearDown(self) -> None:
        """
        This is run after each test run
        :return:
        """

        time.sleep(GRACE_PERIOD)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        This is run only once, when all tests are finished
        :return:
        """
        # remove the created folder
        shutil.rmtree(cls._OUTPUT_PATH)
