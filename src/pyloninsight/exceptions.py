class PylonInsightError(Exception):
    pass


class ParseError(PylonInsightError):
    pass


class UnsupportedHardwareError(PylonInsightError):
    pass