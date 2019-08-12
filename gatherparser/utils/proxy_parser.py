# encoding: utf-8 #
import re
from bs4 import BeautifulSoup
from ..logging import get_loggger
from ..errors.proxy_parser import ProxyParserFetchError, ProxyParserDOMError


class ProxyParser:
    def __init__(self, driver):
        self.driver = driver
        self._logger = get_loggger(self.__class__.__name__)

    def _get_show_full_list_button(self):
        BUTTON_SELECTOR = """input[type="submit"][value="Show Full List"][class="button"]"""
        try:
            button = self.driver.find_element_by_css_selector(BUTTON_SELECTOR)
        except Exception as no_such_element_exc:
            self._logger.error(str(no_such_element_exc))
            raise ProxyParserDOMError('Button with value "Show Full List" not found')
        self._logger.info('Button with value "Show Full List" found')
        return button

    def _load_page_by_url(self, url: str):
        try:
            self.driver.get(url)
        except Exception as get_exc:
            self._logger.error(str(get_exc))
            raise ProxyParserFetchError(f'Selenium unable to open page "{url}"')
        self._logger.info(f'Selenium open page "{url}"')

    def _remove_status_box(self):
        stats_box_element = self.driver.find_element_by_class_name(name="stats-box")
        if not stats_box_element:
            self._logger.error(f'Selenium unable to find element with classname "stats-box"')
            raise ProxyParserDOMError(f'Selenium unable to find element with classname "stats-box"')
        try:
            self.driver.execute_script("arguments[0].remove();", stats_box_element)
        except Exception as execute_exc:
            self._logger.error(str(execute_exc))
            raise ProxyParserDOMError('Error executing element with classname "stats-box" remove script')
        self._logger.info(f'Selenium remove element with classname "stats-box"')

    def _click_show_full_list_button(self):
        show_full_list_button = self._get_show_full_list_button()
        try:
            show_full_list_button.click()
        except Exception as click_exc:
            self._logger.error(str(click_exc))
            raise ProxyParserDOMError('Selenium unable to click on "Show Full List" button')
        self._logger.info('Selenium clicked on "Show Full List" button')

    def _open_full_list_page(self, url_to_open):
        self._load_page_by_url(url=url_to_open)
        self._remove_status_box()
        self._click_show_full_list_button()
        self._logger.info(f'Page {url_to_open} loading done')

    def _get_html_by_page_number(self, page_number):
        try:
            self.driver.execute_script(f"gp.pageClick({page_number});")
        except Exception as execute_exc:
            self._logger.error(str(execute_exc))
            raise ProxyParserFetchError(f'Selenium unable to open page with number "{page_number}"')
        self._logger.info(f'Selenium open page with number "{page_number}"')
        return self.driver.page_source

    def _get_proxies_from_page_html(self, page_html):
        page_source_soup = BeautifulSoup(page_html, "lxml")
        collected_proxies = set()
        table_rows = page_source_soup.select("#tblproxy")[0].tbody.find_all("tr")
        for table_row in table_rows:
            if len(table_row.find_all("td")) != 8:
                continue
            proxy_ip, proxy_port = table_row.find_all("td")[1:3]
            proxy_ip = re.search(r"[\d\.]{2,}$", proxy_ip.text).group(0)
            proxy_port = re.search(r"[\d]{2,}$", proxy_port.text).group(0)
            proxy = ":".join((proxy_ip, proxy_port))
            collected_proxies.add(proxy)

        return collected_proxies

    def _get_proxies_by_page_number(self, page_number):
        page_html = self._get_html_by_page_number(page_number=page_number)
        try:
            proxies = self._get_proxies_from_page_html(page_html=page_html)
        except Exception as table_parse_exc:
            self._logger.error(str(table_parse_exc))
            raise ProxyParserDOMError("Table parse error - bad format")

        self._logger.info(f'Table with proxies from page with number "{page_number}" parsed')
        return proxies

    def get_proxies_by_page_count(self, page_count: int, url_to_parse: str):
        self._open_full_list_page(url_to_open=url_to_parse)
        parsed_proxy = set()

        for page_num in range(1, page_count + 1):
            page_proxies = self._get_proxies_by_page_number(page_number=page_num)
            if page_proxies:
                parsed_proxy = set.union(parsed_proxy, page_proxies)

        self.driver.close()
        return parsed_proxy
