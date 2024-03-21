import random
import asyncio
import time

from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor

import aiomultiprocess


def convert_number_standard(value):
    sleep_time = random.randint(1, 3)
    print('value: {}, sleep: {}'.format(value, sleep_time))
    time.sleep(sleep_time)
    print('{} done'.format(value))
    return value


async def convert_number(value):
    sleep_time = random.randint(1, 3)
    print('value: {}, sleep: {}'.format(value, sleep_time))
    await asyncio.sleep(sleep_time)
    print('{} done'.format(value))
    return value


async def slow_thread_pool():
    # Work in slow speed
    executor = ThreadPoolExecutor(1)
    for result in executor.map(convert_number_standard, range(10)):
        print('output {}'.format(result))


async def normal_process_pool():
    # Work in normal speed
    executor = Pool(4)
    for result in executor.map(convert_number_standard, range(10)):
        print('output {}'.format(result))


async def fast_thread_pool():
    # Work in fast speed
    executor = ThreadPoolExecutor(1)
    for result in await asyncio.gather(*executor.map(convert_number, range(10))):
        print('output {}'.format(result))


async def aio_process_pool():
    # Work in fast speed
    results = []
    t = time.time()
    async with aiomultiprocess.Pool(1) as pool:
        async for result in pool.map(convert_number, range(10)):
            print('output {}'.format(result))
            results.append(result)

        print('cost: {} s '.format(time.time() - t))


if __name__ == '__main__':
    asyncio.run(slow_thread_pool())
    asyncio.run(normal_process_pool())
    asyncio.run(fast_thread_pool())
    asyncio.run(aio_process_pool())
