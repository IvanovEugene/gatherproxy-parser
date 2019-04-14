# gatherproxy-parser
Parser of one of the largest sites with proxies - gatherproxy.com 

## Installation
```bash
python3 setup.py install
```

## Usage
### Chromedriver
```python
from gatherparser import ProxyCollector


driver_kwargs = {
    "driver_path": "path_to_chromedriver",
    "page_load_timeout": 60
}

validator_kwargs = {
    "proxy_verification_link": "https://google.com",
    "proxy_timeout": 30,
    "n_jobs": 100
}

collector_kwargs = {
    "url_to_parse": "http://www.gatherproxy.com/proxylist/country/?c=Russia",
    "page_count": 5,
    "driver_type": "chrome",
    "driver_kwargs": driver_kwargs,
    "validator_kwargs": validator_kwargs
}

proxy_collector = ProxyCollector(**collector_kwargs)
proxies = proxy_collector.collect_proxies()
```
### Example
```bash
python3 examples/chromedriver_mac.py 
```