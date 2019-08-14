# encoding: utf-8
from ..utils.drivers import ChromeDriver
from ..utils.proxy_validator import ProxyValidator
from ..utils.proxy_parser import ProxyParser
from ..logging import get_logger


class ProxyCollector:
    driver_classes = {
        "chrome": ChromeDriver
    }

    def __init__(self, url_to_parse: str, page_count: int, driver_type: str,
                 driver_kwargs: dict, validator_kwargs: dict):
        driver_initializer = self.driver_classes[driver_type](**driver_kwargs)
        driver = driver_initializer.get_driver()
        self._proxy_parser = ProxyParser(driver=driver)
        self._proxy_validator = ProxyValidator(**validator_kwargs)
        self._url_to_parse = url_to_parse
        self._page_count = page_count
        self._logger = get_logger(self.__class__.__name__)

    async def collect_proxies(self):
        proxies = self._proxy_parser.get_proxies_by_page_count(
            page_count=self._page_count, url_to_parse=self._url_to_parse)
        self._logger.info("Proxies collected. Starting to validate")
        valid_proxies = await self._proxy_validator.get_available_proxies(proxies_to_check=proxies)
        self._logger.info("Proxies validated")
        return valid_proxies
