# encoding: utf-8
from abc import ABC, abstractmethod
from selenium import webdriver


class AbstractDriver(ABC):
    @abstractmethod
    def get_driver(self):
        pass


class ChromeDriver(AbstractDriver):
    _WINDOW_SIZE = "1920,1080"

    def __init__(self, driver_path, page_load_timeout=None):
        self._page_load_timeout = page_load_timeout
        self._driver_path = driver_path

    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size={self._WINDOW_SIZE}")

        driver = webdriver.Chrome(executable_path=self._driver_path,
                                  chrome_options=chrome_options)
        if self._page_load_timeout:
            driver.set_page_load_timeout(self._page_load_timeout)

        return driver
