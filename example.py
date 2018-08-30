from gatherproxy_parser import ProxyParser

proxy_parser = ProxyParser(proxy_verification_link="https://www.yandex.ru/", driver_path="chromedriver\\chromedriver.exe")
correct_proxies = proxy_parser.get_several_pages_proxies(parced_url="http://www.gatherproxy.com/proxylist/anonymity/?t=Elite",
                                                         page_count=3)

with open("correct_proxies.txt", mode="w", encoding="utf8") as out:
    for proxy_ip in correct_proxies:
        out.write("{}\n".format(proxy_ip))