# from exceptions import CustomException, CRITICAL


CRITICAL = 50
ERROR = 40
NOTSET = 0


# Any new custom exceptions should extend this on app level
class CustomException(Exception):
    severity = CRITICAL

    def __init__(self, detail=None, extra=None):
        self.detail = detail
        self.extra = extra

    def __str__(self):
        error_message = {'DETAIL': self.detail}
        if self.extra:
            error_message['EXTRA'] = self.extra
        return '\n' + str(error_message)


class InvalidApiKeyException(CustomException):
    severity = CRITICAL
    default_detail = 'INVALID_API_KEY_EXCEPTION'

    def __init__(self, detail=None, extra=None):
        detail = detail or self.default_detail
        super(InvalidApiKeyException, self).__init__(detail=detail, extra=extra)


class WrongInputValueException(CustomException):
    severity = CRITICAL
    default_detail = 'WRONG_INPUT_VALUE_EXCEPTION'

    def __init__(self, detail=None, extra=None):
        detail = detail or self.default_detail
        super(WrongInputValueException, self).__init__(detail=detail, extra=extra)


class AlphaVantageApiException(CustomException):
    severity = CRITICAL
    default_detail = 'ALPHA_VANTAGE_API_EXCEPTION'

    def __init__(self, detail=None, extra=None):
        detail = detail or self.default_detail
        super(AlphaVantageApiException, self).__init__(detail=detail, extra=extra)
