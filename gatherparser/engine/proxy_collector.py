# encoding: utf-8
from ..engine.drivers import ChromeDriver
from ..engine.proxy_validator import ProxyValidator
from ..engine.proxy_parser import ProxyParser
from gatherparser.utils.logging import Logging


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
        self._logger = Logging.get_logger(__name__)

    async def collect_proxies(self):
        proxies = self._proxy_parser.get_proxies_by_page_count(
            page_count=self._page_count, url_to_parse=self._url_to_parse)
        self._logger.info("Proxies collected. Starting to validate")
        valid_proxies = await self._proxy_validator.get_available_proxies(proxies_to_check=proxies)
        self._logger.info("Proxies validated")
        return valid_proxies
