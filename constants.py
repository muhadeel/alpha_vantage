DEFAULT_OUTPUT_FOLDER = 'output'
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co'
GRACE_PERIOD = 20  # 20 second between each test, because the alpha vantage api allows only 5 requests per 1 minute


class AlphaVantageKeys(object):
    ERR_KEY = 'Error Message'
    NOTE_KEY = 'Note'
    SEARCH_KEY = 'bestMatches'
    GLOBAL_QUOTE_KEY = 'Global Quote'
    TIME_SERIES_KEY = 'Time Series'
    TECHNICAL_ANALYSIS_KEY = 'Technical Analysis'


class AlphaVantageFunctions(object):
    SEARCH = 'SYMBOL_SEARCH'
    INTRADAY = 'TIME_SERIES_INTRADAY'
    DAILY = 'TIME_SERIES_DAILY'
    WEEKLY = 'TIME_SERIES_WEEKLY'
    MONTHLY = 'TIME_SERIES_MONTHLY'
    CURRENT_QOUTE = 'GLOBAL_QUOTE'
    EMA = 'EMA'


class AlphaVantageValues(object):
    TIME_INTERVALS_MAP = ['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly']
    SERIES_TYPE_MAP = ['close', 'open', 'high', 'low']
    OUTPUT_SIZE = ['compact', 'full']
    OUTPUT_FORMAT = ['json', 'csv']
