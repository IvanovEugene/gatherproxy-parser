# encoding: utf-8
class ProxyParserException(Exception):
    """Abstract ProxyParser exception"""
    pass


class ProxyParserFetchError(ProxyParserException):
    """Raised when Selenium unable to open page"""
    pass


class ProxyParserDOMError(ProxyParserException):
    """Raised when Selenium unable to find
    required element in Document Object Model"""
    pass
