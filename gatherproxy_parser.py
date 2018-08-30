from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests as rq
import regex


class ChromiumDriver():

    def __init__(self, page_load_timeout, driver_path):
        self.page_load_timeout = page_load_timeout
        self.driver_path = driver_path

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(
            self.driver_path, chrome_options=chrome_options)
        driver.set_page_load_timeout(self.page_load_timeout)
        return driver
    
    
class ProxyParser():
    
    def __init__(self, proxy_verification_link, driver_path, proxy_timeout=10, selenium_timeout=60, n_jobs=0):
        self.proxy_timeout = proxy_timeout
        self.proxy_verification_link = proxy_verification_link
        self.n_jobs = n_jobs
        self.__chromium_driver = ChromiumDriver(driver_path=driver_path, 
                                              page_load_timeout=selenium_timeout)
        
    def __del__(self):
        del self.__chromium_driver
    
    def __prepare_parced_page(self):
        try:
            stats_box_element = self.chrome_driver.find_element_by_class_name("stats-box")
            self.chrome_driver.execute_script("arguments[0].remove();", stats_box_element)
        except:
            pass
        show_full_button = self.chrome_driver.find_element_by_class_name("button")
        show_full_button.click()

    def __get_parced_page(self, page_num):
        self.chrome_driver.execute_script("gp.pageClick({});".format(page_num))
        page_source = self.chrome_driver.page_source
        page_source_soup = bs(page_source, "lxml")
        collected_proxies = set()
        table_lines = page_source_soup.select("#tblproxy")[0].tbody.find_all("tr")
        for table_line in table_lines:
            if len(table_line.find_all("td")) != 8:
                continue
            proxy_ip, proxy_port = table_line.find_all("td")[1:3]
            proxy_ip, proxy_port = (regex.search("[\d.]{2,}$", proxy_ip.text).group(0),
                                    regex.search("[\d]{2,}$", proxy_port.text).group(0))
            full_proxy_ip = ":".join([proxy_ip, proxy_port])
            collected_proxies.add(full_proxy_ip)
        return collected_proxies
    
    def get_several_pages_proxies(self, page_count, parced_url):
        self.chrome_driver = self.__chromium_driver.start_driver()
        proxy_to_validate = set()
        self.chrome_driver.get(parced_url)
        self.__prepare_parced_page()
        for page in range(1, page_count + 1):
            page_proxies = self.__get_parced_page(page_num=page)
            if page_proxies:
                proxy_to_validate = set.union(proxy_to_validate, page_proxies)

        self.chrome_driver.quit()
        pool = ThreadPool(len(proxy_to_validate)) if not self.n_jobs else ThreadPool(self.n_jobs)
        proxy_validator = ProxyValidator(proxy_timeout=self.proxy_timeout, proxy_verification_link=self.proxy_verification_link)
        validate_result = pool.map(proxy_validator.validate_proxy, proxy_to_validate)
        del proxy_validator
        pool.close()
        pool.join()
        validate_result = {proxy_ip for proxy_ip in validate_result if proxy_ip}

        return validate_result
    
    
class ProxyValidator():
    
    def __init__(self, proxy_timeout, proxy_verification_link):
        self.proxy_verification_link = proxy_verification_link
        self.proxy_timeout = float(proxy_timeout)

    def validate_proxy(self, proxy_ip):
        if not proxy_ip:
            return False
        try:
            proxy_request=rq.get(self.proxy_verification_link, timeout=self.proxy_timeout,
                                proxies={"http": proxy_ip,"https": proxy_ip})
            if proxy_request.status_code != 200:
                raise
            return proxy_ip
        except:
            return False