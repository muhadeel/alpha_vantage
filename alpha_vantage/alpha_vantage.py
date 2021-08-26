import inspect
from typing import Optional, Dict, Union, List

import requests

from constants import AlphaVantageFunctions, AlphaVantageValues, ALPHA_VANTAGE_BASE_URL, AlphaVantageKeys
from helpers.custom_exceptions_helper import InvalidApiKeyException, AlphaVantageApiException
from helpers.decorators.validation_decorator import validate_interval, validate_result, validate_series_type


class AlphaVantage(object):
    """ Base class for the alpha vantage api
    """
    _ALPHA_VANTAGE_BASE_URL = ALPHA_VANTAGE_BASE_URL
    _FUNCTIONS = AlphaVantageFunctions()
    _KEYS = AlphaVantageKeys()
    _VALUES = AlphaVantageValues()

    def __init__(self, key: str, output_format='json', output_size='compact'):
        """ Initialize the class
        :param key:
        :param output_format:
        :param output_size:
        """
        self.output_format = output_format
        self.output_size = output_size
        self.set_api_key(key)

    def set_api_key(self, api_key: str) -> None:
        """ Sets the api key, if it is invalid, will raise InvalidApiKeyException.
        :param api_key:
        :raises InvalidApiKeyException:
        :return:
        """
        self.api_key = api_key
        # test the api key by using the api search

        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.SEARCH}&keywords=test' \
              f'&apikey={self.api_key}'
        request = requests.get(url)
        result = request.json()

        if self._KEYS.ERR_KEY in result.keys():
            raise InvalidApiKeyException(extra=result[self._KEYS.ERR_KEY])
        return None

    def search(self, keyword: str, force_json: bool = True) -> Union[List[Dict[str, str]], bytes]:
        """ Look for the best-matching symbols and market information based on the passed keyword.
        :param keyword:
        :param force_json: force using json here, to display in the console each search
        :raises AlphaVantageApiException:
        :return:
        """
        # must force json here, to display in the console each search
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.SEARCH}&keywords={keyword}' \
              f'&apikey={self.api_key}&datatype={output_format}'

        request = requests.get(url)
        result = request.json()

        if output_format == 'json':
            if self._KEYS.SEARCH_KEY not in result.keys():
                raise AlphaVantageApiException(extra=f'No result found, invalid keyword:`{keyword}`')
            result = result[self._KEYS.SEARCH_KEY]
        return result

    @validate_result
    def get_current_quote(self, symbol: str, force_json: bool = True):
        """ Extract the current quotes for a given symbol.
        :param symbol:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.CURRENT_QOUTE}&symbol={symbol}' \
              f'&apikey={self.api_key}&datatype={output_format}'

        result = self._get_result_per_output_format(url=url, key=self._KEYS.GLOBAL_QUOTE_KEY,
                                                    output_format=output_format)
        return result

    @validate_series_type
    @validate_interval
    @validate_result
    def get_ema(self, symbol: str, interval: str, time_period: int, series_type: str,
                force_json: bool = True) -> Union[Dict[str, Dict[str, str]], bytes]:
        """ Get exponential moving average for a given interval, aggregated by time period
        :param symbol:
        :param interval:
        :param time_period: moving average window
        :param series_type:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.EMA}&symbol={symbol}' \
              f'&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}' \
              f'&datatype={output_format}'

        result = self._get_result_per_output_format(
            url=url,
            output_format=output_format,
            key=f'{self._KEYS.TECHNICAL_ANALYSIS_KEY}: {AlphaVantageFunctions.EMA}')
        return result

    @validate_interval
    @validate_result
    def get_intraday(self, symbol: str, interval: str, adjusted: Optional[bool] = True,
                     force_json: bool = False) -> Union[Dict[str, Dict[str, str]], bytes]:
        """ Get intraday time series of the equity specified, covering extended trading hours where applicable.
        :param symbol:
        :param interval:
        :param adjusted:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.INTRADAY}&symbol={symbol}' \
              f'&interval={interval}&apikey={self.api_key}&adjusted={str(adjusted).lower()}' \
              f'&outputsize={self.output_size}&datatype={output_format}'

        result = self._get_result_per_output_format(url=url, key=f'{self._KEYS.TIME_SERIES_KEY} ({interval})',
                                                    output_format=output_format)
        return result

    @validate_result
    def get_daily_timeseries(self, symbol: str, force_json: bool = False) -> Union[Dict[str, Dict[str, str]], bytes]:
        """ Get daily time series of the global equity specified, covering 20+ years of historical data
        :param symbol:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.DAILY}&symbol={symbol}' \
              f'&apikey={self.api_key}&datatype={output_format}'

        result = self._get_result_per_output_format(url=url, key=f'{self._KEYS.TIME_SERIES_KEY} (Daily)',
                                                    output_format=output_format)
        return result

    @validate_result
    def get_weekly_timeseries(self, symbol: str, force_json: bool = False) -> Union[Dict[str, Dict[str, str]], bytes]:
        """ Get weekly time series of the global equity specified, covering 20+ years of historical data
        :param symbol:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.WEEKLY}&symbol={symbol}' \
              f'&apikey={self.api_key}&datatype={output_format}'

        result = self._get_result_per_output_format(url=url, key=f'Weekly {self._KEYS.TIME_SERIES_KEY}',
                                                    output_format=output_format)
        return result

    @validate_result
    def get_monthly_timeseries(self, symbol: str, force_json: bool = False) -> Union[Dict[str, Dict[str, str]], bytes]:
        """ Get monthly time series of the global equity specified, covering 20+ years of historical data
        :param symbol:
        :param force_json: must force json here, to display in the console each search
        :return:
        """
        output_format = 'json' if force_json else self.output_format
        url = f'{self._ALPHA_VANTAGE_BASE_URL}/query?function={self._FUNCTIONS.MONTHLY}&symbol={symbol}' \
              f'&apikey={self.api_key}&datatype={output_format}'

        result = self._get_result_per_output_format(url=url, key=f'Monthly {self._KEYS.TIME_SERIES_KEY}',
                                                    output_format=output_format)
        return result

    def _get_result_per_output_format(self, url: str, key: Optional[str] = None,
                                      output_format: Optional[str] = None) -> Union[Dict, bytes]:
        """ Used when getting either csv or json output.
        :param url:
        :param output_format: json or csv
        :param key: the key in the result dictionary that contains the required data.
        :return:
        """
        if output_format is None:
            output_format = self.output_format

        result = None

        if output_format == 'json':
            request = requests.get(url)
            result_json = request.json()
            if key not in list(result_json.keys()):
                caller_func = inspect.stack()[1][3]
                raise AlphaVantageApiException(extra=f'No result found, could not perform {caller_func}')
            result = result_json[key]

        elif output_format == 'csv':
            request = requests.get(url, allow_redirects=True)
            result = request.content

        return result
