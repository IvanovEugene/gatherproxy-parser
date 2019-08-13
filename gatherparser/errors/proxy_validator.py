# encoding: utf-8
class ProxyValidatorException(Exception):
    """Abstract ProxyValidator exception"""
    pass


class ProxyValidatorWrongFormatError(ProxyValidatorException):
    """Raises when proxy has wrong format (missing port or other)"""
    pass
