import asyncio
import http
from asyncio import FIRST_COMPLETED, CancelledError
from time import time
from dataclasses import dataclass
from typing import Union

import aiohttp
from aiohttp import ClientSession
from loguru import logger


@dataclass
class Service:
    name: str
    url: str
    ip_field: str


SERVICES = [
    Service('ipify', 'https://api.ipify.org/?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
]


async def fetch(session: ClientSession, url: str) -> dict:
    """
    :param session
    :param url
    :return:
    """
    async with session.get(url) as response:
        return await response.json()


async def fetch_ip(service: Service) -> str:
    """
    :param service
    :return
    """
    my_ip = 'not  found'

    logger.info('Starting with {}', service.name)
    start = time()
    try:
        async with aiohttp.ClientSession() as session:
            json = await fetch(session, service.url)
            end = time()
            logger.info('Got answer from {} after {:.3f}s', service.name, end - start)
    except CancelledError as exc:
        # logger.debug('Canceled fetching {!r}', service.name, exc_info=e)
        # logger.exception('Canceled fetching {!r}', service.name, exc_info=e)
        logger.opt(exception=exc).debug('Canceled fetching {!r}', service.name)
        return 'Cancelled'
    except Exception:
        logger.exception('Error with {}', service)
        return 'error'
    try:
        my_ip = json[service.ip_field]
    except KeyError:
        logger.exception("Couldn't get ip from {} using field {}",
                         json, service.ip_field)
    return my_ip


async def fetch_ip_fastest(timeout: Union[int, float]) -> str:
    """
    :return
    """
    my_ip = 'No result'
    futures = [fetch_ip(s) for s in SERVICES]
    # res = await asyncio.wait(futures)
    done, pending = await asyncio.wait(
        futures,
        timeout=timeout,
        return_when=FIRST_COMPLETED,
    )

    # logger.info('Done: {}', done)
    # logger.info('Pending: {}', pending)

    for fut in pending:
        fut.cancel()

    for fut in done:
        my_ip = fut.result()
        break
    else:
        logger.warning('Could not fetch any results in {}s', timeout)

    # logger.info('Done: {}', done)
    # logger.info('Pending: {}', pending)
    # logger.info('res from all: {}', res)
    return my_ip


def main():
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(fetch_ip_fastest(1))
    loop.close()
    logger.info('Result from loop: {!r}', res)


if __name__ == '__main__':
    main()
