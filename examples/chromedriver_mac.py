# encoding: utf-8 #
import os
from gatherparser import ProxyCollector


if __name__ == "__main__":
    URL_TO_PARSE = "http://www.gatherproxy.com/proxylist/country/?c=Russia"
    PAGE_COUNT = 5
    DRIVER_TYPE = "chrome"

    driver_kwargs = {
        "driver_path": os.path.join("tools", "drivers", "chrome",
                                    "macOS", "chromedriver"),
        "page_load_timeout": 60
    }
    validator_kwargs = {
        "proxy_verification_link": "https://google.com",
        "proxy_timeout": 30,
        "n_jobs": 100
    }

    collector_kwargs = {
        "url_to_parse": URL_TO_PARSE,
        "page_count": PAGE_COUNT,
        "driver_type": DRIVER_TYPE,
        "driver_kwargs": driver_kwargs,
        "validator_kwargs": validator_kwargs
    }

    proxy_collector = ProxyCollector(**collector_kwargs)
    valid_proxies = proxy_collector.collect_proxies()
    print(valid_proxies)