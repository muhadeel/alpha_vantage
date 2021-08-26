import json
import os
import re
import time
from typing import Dict, List, Union

from alpha_vantage.alpha_vantage import AlphaVantage
from constants import AlphaVantageValues, AlphaVantageFunctions
from helpers.custom_exceptions_helper import WrongInputValueException, AlphaVantageApiException


class AplhaAdvantageRunner(object):
    def __init__(self, api_key: str, output_dest: str, output_format: str = 'json',
                 output_size: str = 'compact', verbose: bool = False):
        """ Initialize the class
        :param api_key:
        :param output_dest:
        :param output_format:
        :param output_size:
        """
        self.alpha_vantage = AlphaVantage(key=api_key, output_format=output_format, output_size=output_size)
        self.output_dest = output_dest
        self.verbose = verbose

    def run(self):
        """ Run the interactive cli applciation.
        :return:
        """
        while True:
            # first, search companies
            result = self._search()
            print('{:*^40}'.format('Search Result'))
            for i, entry in enumerate(result):
                print('{:>2}.{:<20}{}'.format(i + 1, entry['1. symbol'], entry['2. name']))

            # select a company to perform further analysis
            index = input("Select a company number, or (q) to exit:\n")
            index = self.__parse_input(index, len(result))
            company = result[index - 1]

            option = input("Select an action, or (q) to exit:\n"
                           "1. Display additional details in grid.\n"
                           "2. Display historical prices on specific timeframes.\n"
                           "3. Display current quote.\n"
                           "4. Display exponential moving average.\n")

            option = self.__parse_input(option, 4)

            symbol = company['1. symbol']
            if option == 1:
                print('{:*^40}'.format('Additional details'))
                self.__display_dictionary_info(dict_object=company)
            elif option == 2:
                self._display_historical_prices(symbol=symbol)
            elif option == 3:
                print('{:*^40}'.format('Current Quote:'))
                result = self._get_quote(symbol=symbol)
                if result:
                    self.__display_dictionary_info(dict_object=result)
            elif option == 4:
                result = self._get_ema(symbol=symbol)
                if result:
                    self.__display_dictionary_info(dict_object=result, sub=False)
            option = input("Enter any key to restart again, or (q) to exit:\n")
            if option == 'q':
                exit()

    def _search(self) -> List[Dict[str, str]]:
        """ Use alpha vantage search api and display the result
        :return:
        """
        keyword = input("Enter a keyword\n")
        result = self.alpha_vantage.search(keyword=keyword, force_json=True)
        if len(result) == 0:
            print('No match found.')
            exit()
        return result

    def _intraday(self, symbol: str, interval: str) -> Union[Dict, bytes]:
        """ Get intraday time series data for a company according the given interval.
        :param interval:
        :param symbol:
        :return:
        """
        if interval not in AlphaVantageValues.TIME_INTERVALS_MAP:
            raise WrongInputValueException(extra=f'`interval` should be one of following: '
                                                 f'{AlphaVantageValues.TIME_INTERVALS_MAP}, {interval} is not accepted.')
        result = self.alpha_vantage.get_intraday(symbol=symbol, interval=interval)
        return result

    def _daily(self, symbol: str) -> Union[Dict, bytes]:
        """ Get daily time series data for a company according the given interval.
        :param symbol:
        :return:
        """
        return self.alpha_vantage.get_daily_timeseries(symbol=symbol)

    def _weekly(self, symbol: str) -> Union[Dict, bytes]:
        """ Get weekly time series data for a company according the given interval.
        :param symbol:
        :return:
        """
        return self.alpha_vantage.get_weekly_timeseries(symbol=symbol)

    def _monthly(self, symbol: str) -> Union[Dict, bytes]:
        """ Get monthly time series data for a company according the given interval.
        :param symbol:
        :return:
        """
        return self.alpha_vantage.get_monthly_timeseries(symbol=symbol)

    def _get_quote(self, symbol: str) -> Dict[str, str]:
        """ Get current quote for this company
        :param symbol:
        :return:
        """
        result = None
        try:
            result = self.alpha_vantage.get_current_quote(symbol=symbol, force_json=True)
        except AlphaVantageApiException:
            print('No quote found.')
        return result

    def _get_ema(self, symbol: str) -> Dict[str, str]:
        """ Get exponential moving average for a given interval, aggregated by time period
        :param symbol:
        :return:
        """
        interval = input(f"Enter an interval, options: {AlphaVantageValues.TIME_INTERVALS_MAP}:\n")
        if interval not in AlphaVantageValues.TIME_INTERVALS_MAP:
            raise WrongInputValueException(extra=f'`interval` should be one of following: '
                                                 f'{AlphaVantageValues.TIME_INTERVALS_MAP}, {interval} is not accepted.')

        time_period = input(f"Enter an time period, number of data points used to calculate each moving average value "
                            f"e.g., 60, 200, ... etc):\n")
        try:
            time_period = int(time_period)
            if time_period < 1:
                raise ValueError()
        except ValueError:
            raise WrongInputValueException(extra='Wrong input, should be positive integer.')

        series_type = input(f"Enter a series type, options: {AlphaVantageValues.SERIES_TYPE_MAP}:\n")
        if series_type not in AlphaVantageValues.SERIES_TYPE_MAP:
            raise WrongInputValueException(extra=f'`series type` should be one of following: '
                                                 f'{AlphaVantageValues.SERIES_TYPE_MAP}, {series_type} is not accepted.')

        result = None
        try:
            result = self.alpha_vantage.get_ema(symbol=symbol, interval=interval, series_type=series_type,
                                                time_period=time_period, force_json=True)
        except AlphaVantageApiException:
            print('No data found.')
        formatted_results = None
        if result:
            formatted_results = {}
            for key, value in result.items():
                formatted_results[key] = value[AlphaVantageFunctions.EMA]
        return formatted_results

    def _display_historical_prices(self, symbol: str) -> None:
        """

        :param symbol:
        :return:
        """
        option = input("Select the form of temporal resolution to display, or (q) to exit:\n" +
                       "\n".join([f'{i + 1}. {interval}' for i, interval in
                                  enumerate(AlphaVantageValues.TIME_INTERVALS_MAP)]) +
                       "\n")

        option = self.__parse_input(option, len(AlphaVantageValues.TIME_INTERVALS_MAP))
        result = None
        try:
            if option >= 1 and option <= 5:
                result = self._intraday(symbol=symbol, interval=AlphaVantageValues.TIME_INTERVALS_MAP[option - 1])
            elif option == 6:
                result = self._daily(symbol=symbol)
            elif option == 7:
                result = self._weekly(symbol=symbol)
            elif option == 8:
                result = self._monthly(symbol=symbol)
        except AlphaVantageApiException:
            print('No result found')

        if result:
            self.__print_and_save_result(symbol=symbol, interval=AlphaVantageValues.TIME_INTERVALS_MAP[option - 1],
                                         result=result)
        return None

    @staticmethod
    def __display_dictionary_info(dict_object: Dict[str, str], sub: bool = True) -> None:
        """

        :param dict_object:
        :param sub: True if key needs cleaning (remove ordered numbers 1., 2. .. etc)
        :return:
        """
        for key, value in dict_object.items():
            if sub:
                print('{:<20}{}'.format(re.sub("[^a-zA-Z]", "", key), value))
            else:
                print('{:<20}{}'.format(key, value))
        return None

    def __print_and_save_result(self, symbol: str, interval: str, result: Union[Dict, bytes]):
        """

        :param symbol:
        :param interval:
        :param result:
        :return:
        """
        if self.alpha_vantage.output_format == 'json':
            timestamp = time.time()
            file_name = os.path.join(self.output_dest, f'{symbol}_{interval}_{timestamp}.json')
            with open(file_name, "w") as outfile:
                json.dump(result, outfile, indent=4, sort_keys=True)
            if self.verbose and self.alpha_vantage.output_format == 'json':
                for key, value in result.items():
                    print(f'{key}:')
                    self.__display_dictionary_info(dict_object=value)

        elif self.alpha_vantage.output_format == 'csv':
            timestamp = time.time()
            file_name = os.path.join(self.output_dest, f'{symbol}_{type}_{timestamp}.csv')
            with open(file_name, "wb") as outfile:
                outfile.write(result)
        return None

    def __parse_input(self, option, max_option: int) -> int:
        """

        :param option:
        :param max_option:
        :return:
        """
        if option == 'q':
            exit()
        try:
            option = int(option)
            if option > max_option or option < 1:
                raise ValueError()
        except ValueError:
            option = input(f'Please choose one of the displayed numbers, {option} is not listed, or (q) to exit:\n')
            self.__parse_input(option, max_option)
        return option
