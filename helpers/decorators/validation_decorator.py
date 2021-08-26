from functools import wraps

from constants import AlphaVantageKeys, AlphaVantageValues
from helpers.custom_exceptions_helper import WrongInputValueException, AlphaVantageApiException


def validate_interval(func):
    """
    Decorator to validate the passed interval
    func:  The function to be decorated
    """

    @wraps(func)
    def _validate_interval_wrapper(*args, **kwargs):
        """
        Validates if the given interval value is allowed.
        :raises WrongInputException:
        :return:
        """
        interval = kwargs['interval']
        if interval not in AlphaVantageValues.TIME_INTERVALS_MAP:
            raise WrongInputValueException(extra=f'`interval` should be one of following: '
                                                 f'{AlphaVantageValues.TIME_INTERVALS_MAP}\n'
                                                 f'{interval} is not accepted.')
        return func(*args, **kwargs)

    return _validate_interval_wrapper


def validate_series_type(func):
    """
    Decorator to validate the passed series type
    func:  The function to be decorated
    """

    @wraps(func)
    def _validate_series_type_wrapper(*args, **kwargs):
        """
        Validates if the given series type value is allowed.
        :raises WrongInputException:
        :return:
        """
        series_type = kwargs['series_type']
        if series_type not in AlphaVantageValues.SERIES_TYPE_MAP:
            raise WrongInputValueException(extra=f'`series_type` should be one of following: '
                                                 f'{AlphaVantageValues.SERIES_TYPE_MAP}, {series_type} is not accepted.')
        return func(*args, **kwargs)

    return _validate_series_type_wrapper


def validate_result(func):
    @wraps(func)
    def _validate_result_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        data = None
        if isinstance(result, dict):
            data = result.keys()
        elif isinstance(result, bytes):
            data = result.decode("utf-8")
        if data:
            if AlphaVantageKeys.ERR_KEY in data:
                raise AlphaVantageApiException(extra={
                    'api': func.__name__,
                    'passed_args': kwargs,
                })
            elif AlphaVantageKeys.NOTE_KEY in data:
                raise AlphaVantageApiException(extra={
                    'message': 'Api limit exceeded per minute (5 times) or per day (500 times).'
                })
        return result

    return _validate_result_wrapper
