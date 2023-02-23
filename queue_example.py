from math import factorial
from queue import Queue
from threading import Thread
from loguru import logger
from time import time
import sys
sys.set_int_max_str_digits(0)

THREADS_COUNT = 10
q = Queue()
q2 = Queue()


def worker():
    while 1:
        item = q.get()
        res = factorial(item)
        factorials_length = len(str(res))
        # q2.put(factorials_length)
        # print(factorials_length)
        logger.info('Process {}. Length is {}', item, factorials_length)
        q.task_done()


if __name__ == '__main__':
    logger.info('Starting main')

    for _ in range(THREADS_COUNT):
        thread = Thread(
            target=worker,
            daemon=True,
        )
        thread.start()

    logger.info('Fulfilling queue')
    for item in range(9500, 9900):
        q.put(item)

    logger.info('Waiting..')

    start = time()
    q.join()
    end = time()

    logger.info('it took {:.3f} seconds', end - start)


    logger.info('Finished main')
