# encoding: utf-8
import asyncio
from aiohttp import ClientSession, ClientTimeout
from ..logging import Logging
from gatherparser.utils.exceptions import ProxyValidatorWrongFormatError


class ProxyValidator:
    def __init__(self, proxy_timeout, proxy_verification_link):
        self._proxy_verification_link = proxy_verification_link
        self._proxy_timeout = proxy_timeout
        self._logger = Logging.get_logger(__name__)

    async def _validate_format(self, proxy: str):
        proxy = proxy.split(":")
        if len(proxy) != 2:
            self._logger.error(f"Unable to split proxy to IP and port: {proxy}")
            raise ProxyValidatorWrongFormatError("Unable to split proxy to IP and port")

        ip, port = proxy
        if not (len(ip.split(".")) == 4 and port.isdigit()):
            self._logger.error(f"Bad proxy format: {proxy}")
            raise ProxyValidatorWrongFormatError("Bad proxy format")

        self._logger.debug(f"Proxy {ip}:{port} has the correct format")

    async def _fetch_with_proxy(self, session: ClientSession, proxy: str):
        async with session.get(url=self._proxy_verification_link, proxy=f"http://{proxy}") as response:
            await response.raise_for_status()

    async def _is_proxy_valid(self, session: ClientSession, proxy: str):
        try:
            await self._validate_format(proxy=proxy)
        except ProxyValidatorWrongFormatError:
            return False
        except Exception as other_exc:
            self._logger.error(f"Other proxy format validation error: {other_exc}")
            return False
        try:
            await self._fetch_with_proxy(session=session, proxy=proxy)
        except Exception as async_request_exc:
            exception_class_name = async_request_exc.__class__.__name__
            self._logger.debug(f"Broken proxy: {proxy}. Exception class: {exception_class_name}")
            return False
        self._logger.debug(f"Proxy {proxy} is valid")
        return True

    async def _validate_proxies(self, proxies: set):
        proxies = tuple(proxies)
        async with ClientSession(timeout=ClientTimeout(total=self._proxy_timeout)) as session:
            tasks = [self._is_proxy_valid(session=session, proxy=proxy) for proxy in proxies]
            done, _ = await asyncio.wait(tasks)
        done = tuple(done)
        return set([proxies[i] for i in range(len(proxies)) if done[i]])

    async def get_available_proxies(self, proxies_to_check: set):
        return await self._validate_proxies(proxies=proxies_to_check)
