# import logging
import math
import threading
from multiprocessing.pool import ThreadPool
from time import sleep, time
from loguru import logger
import requests
import sys
sys.set_int_max_str_digits(0)


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


def process_google_results(query: str) -> int:
    url = 'https://www.google.com/search'
    # logger.info(f'Starting searching for {query}')
    logger.info('Starting searching for {!r}', query)
    # logger.info('Starting searching for %s', query)
    response = requests.get(
        url=url,
        params={'q': f'{query}'},
        # timeout=(5, 10),
    )
    logger.info('Got answer for {}', query)
    text = response.text
    # result = parse_search_results_for_query(query, text)
    # save_result_to_db(result)
    sleep(1)
    response_len = len(text)
    logger.info('Finished processing query {!r} with result len {}', query, response_len)
    if response_len > 10_000:
        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception('Error')
            return None
    return response_len


def process_factorial(item: int) -> int:
    factorial = math.factorial(item)
    factorials_lengths = len(str(factorial))
    return factorials_lengths


if __name__ == "__main__":
    logger.info('Starting main')
    # # query = 'python'
    # # process_google_results(query)
    # queries = (
    #     'iphone',
    #     'galaxy',
    #     'huawei',
    # )
    # threads = []
    # for query in queries:
    #     thread = threading.Thread(
    #         target=process_google_results,
    #         args=(query, ),
    #     )
    #     logger.info('query {!r} start', query)
    #     thread.start()
    #     logger.info('query {!r} finish', query)
    #     threads.append((thread, query))
    # #
    # for thread, query in threads:
    #     logger.info('Joining thread {}', query)
    #     thread.join()
    #     logger.info('Finished thread {}', query)
    # thread = threading.Thread(
    #     target=process_google_results,
    #     args=('python',),
    #     daemon=True,
    #     # daemon=False,
    # )
    # thread.start()
    # thread.join()
    queries = (
        'iphone',
        'galaxy',
        'xiaomi',
        'huawei',
        'pycharm',
        'jetbrains',
        'vscode',
        'yandex',
        'google',
    )
    queries *= 2
    factorials_args = range(9500, 9900)
    start = time()
    pool = ThreadPool(9)
    # results = pool.map(process_google_results, queries)
    results = pool.map(process_factorial, factorials_args)
    print(results)
    end = time()

    logger.info('pool took {:.3f} seconds', end - start)
    logger.info('results: {}', results)
    logger.info('Finished main')
