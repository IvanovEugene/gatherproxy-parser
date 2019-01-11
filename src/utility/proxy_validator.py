# encoding: utf-8 #
from multiprocessing.dummy import Pool
from requests import get, status_codes


class ProxyValidator:

    def __init__(self, proxy_timeout, proxy_verification_link, n_jobs):
        self.proxy_verification_link = proxy_verification_link
        self.proxy_timeout = float(proxy_timeout)
        self.n_jobs = n_jobs

    def __is_proxy_works(self, proxy: str):
        if not proxy:
            return False

        try:
            request_proxies = {"http": proxy, "https": proxy}
            proxy_request = get(
                url=self.proxy_verification_link, timeout=self.proxy_timeout,
                proxies=request_proxies)
            if proxy_request.status_code != status_codes.codes.ok:
                return False
            return proxy

        except Exception as request_exception:
            return False

    @staticmethod
    def __is_proxy_format_valid(proxy: str):
        proxy = proxy.split(":")
        if len(proxy) != 2:
            return False

        ip, port = proxy
        if not (len(ip.split(".")) == 4 and port.isdigit()):
            return False

        return True

    def __is_proxy_valid(self, proxy: str):
        if (self.__is_proxy_format_valid(proxy=proxy)
                and self.__is_proxy_works(proxy=proxy)):
            return True

    def get_available_proxies(self, proxies_to_check):
        pool = Pool(self.n_jobs)
        results = zip(proxies_to_check,
                      pool.map(self.__is_proxy_valid, proxies_to_check))
        pool.close()
        pool.join()

        return {proxy for proxy, is_valid in results if is_valid}
