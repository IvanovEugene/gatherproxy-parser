# encoding: utf-8 #
from abc import ABC, abstractmethod
from selenium import webdriver


class AbstractDriver(ABC):

    @abstractmethod
    def get_driver(self):
        pass


class ChromeDriver(AbstractDriver):
    def __init__(self, driver_path, page_load_timeout=None):
        self.page_load_timeout = page_load_timeout
        self.driver_path = driver_path

    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=self.driver_path,
                                  chrome_options=chrome_options)
        if self.page_load_timeout:
            driver.set_page_load_timeout(self.page_load_timeout)

        return driver


class PhantomJSDriver(AbstractDriver):
    def __init__(self, driver_path, page_load_timeout=None):
        self.page_load_timeout = page_load_timeout
        self.driver_path = driver_path

    def get_driver(self):
        driver = webdriver.PhantomJS(executable_path=self.driver_path)
        if self.page_load_timeout:
            driver.set_page_load_timeout(self.page_load_timeout)

        return driver
