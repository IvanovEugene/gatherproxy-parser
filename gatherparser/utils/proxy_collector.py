# encoding: utf-8 #
from ..utils.drivers import ChromeDriver, PhantomJSDriver
from ..utils.proxy_validator import ProxyValidator
from ..utils.proxy_parser import ProxyParser


class ProxyCollector:
    driver_classes = {
        "chrome": ChromeDriver,
        "phantomjs": PhantomJSDriver
    }

    def __init__(self, url_to_parse: str, page_count: int, driver_type: str,
                 driver_kwargs: dict, validator_kwargs: dict):
        driver_initializer = self.driver_classes[driver_type](**driver_kwargs)
        driver = driver_initializer.get_driver()
        self.proxy_parser = ProxyParser(driver=driver)
        self.proxy_validator = ProxyValidator(**validator_kwargs)
        self.url_to_parse = url_to_parse
        self.page_count = page_count

    def collect_proxies(self):
        proxies = self.proxy_parser.get_pages_with_proxy(
            page_count=self.page_count, url_to_parse=self.url_to_parse)
        valid_proxies = self.proxy_validator.get_available_proxies(
            proxies_to_check=proxies)
        return valid_proxies
