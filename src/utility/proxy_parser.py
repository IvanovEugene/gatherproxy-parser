# encoding: utf-8 #
import re
from bs4 import BeautifulSoup


class ProxyParser:

    def __init__(self, driver):
        self.driver = driver

    def __get_show_full_list_button(self):
        elements = self.driver.find_elements_by_tag_name(name="input")
        if not elements:
            return None

        for element in elements:
            if (element.get_attribute("value") == "Show Full List" and
                    element.get_attribute("class") == "button"):
                return element

        return None

    def __load_page_by_url(self, url: str):
        self.driver.get(url)

    def __remove_status_box(self):
        stats_box_element = self.driver.find_element_by_class_name(
            name="stats-box")

        if stats_box_element:
            self.driver.execute_script(
                "arguments[0].remove();", stats_box_element)

            return True
        return False

    def __click_show_full_list_button(self):
        show_full_list_button = self.__get_show_full_list_button()
        if not show_full_list_button:
            return None
        show_full_list_button.click()

    def __open_full_list_page(self, url_to_open):
        self.__load_page_by_url(url=url_to_open)
        self.__remove_status_box()
        if not self.__click_show_full_list_button():
            return None

    def __get_html_by_page_number(self, page_number):
        self.driver.execute_script("gp.pageClick(%s);" % page_number)
        return self.driver.page_source

    def __get_proxies_from_page_html(self, page_html):
        page_source_soup = BeautifulSoup(page_html, "lxml")
        collected_proxies = set()
        table_lines = page_source_soup.select(
            "#tblproxy")[0].tbody.find_all("tr")
        for table_line in table_lines:
            if len(table_line.find_all("td")) != 8:
                continue
            proxy_ip, proxy_port = table_line.find_all("td")[1:3]
            proxy_ip = re.search(r"[\d\.]{2,}$", proxy_ip.text).group(0)
            proxy_port = re.search(r"[\d]{2,}$", proxy_port.text).group(0)
            proxy = ":".join((proxy_ip, proxy_port))
            collected_proxies.add(proxy)

        return collected_proxies

    def __get_proxies_by_page_number(self, page_number):
        page_html = self.__get_html_by_page_number(page_number=page_number)
        proxies = self.__get_proxies_from_page_html(page_html=page_html)

        return proxies

    def get_pages_with_proxy(self, page_count: int, url_to_parse: str):
        self.__open_full_list_page(url_to_open=url_to_parse)
        parsed_proxy = set()

        for page_num in range(1, page_count + 1):
            page_proxies = self.__get_proxies_by_page_number(
                page_number=page_num)
            if page_proxies:
                parsed_proxy = set.union(parsed_proxy, page_proxies)

        self.driver.close()
        return parsed_proxy
