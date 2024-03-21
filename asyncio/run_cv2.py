import os
import time
import string
import random
import asyncio

import cv2


def read_file(image_path):
    return cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)


def write_file(image_path, image_data):
    cv2.imwrite(image_path, image_data)


def main(input_image_path, output_image_dir):
    # This runs in a serial way, so it is slow.
    input_image_data = read_file(input_image_path)
    for index in range(100):
        s = time.time()
        output_image_path = os.path.join(output_image_dir, '{:>04}.png'.format(index))
        write_file(output_image_path, input_image_data)
        print('Cost: {} s'.format(time.time() - s))


async def basic_async_main(input_image_path, output_image_dir):
    # This use asyncio, but did not get any benefit from it
    loop = asyncio.get_event_loop()

    input_image_data = read_file(input_image_path)
    for _ in range(100):
        s = time.time()
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        output_image_path = os.path.join(output_image_dir, '{}.png'.format(random_string))
        await loop.run_in_executor(None, write_file, output_image_path, input_image_data)
        print('Cost: {} s'.format(time.time() - s))


async def write_image(filename, image):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, cv2.imwrite, filename, image)


async def async_main(input_image_path, output_image_dir):
    # This use asyncio and parallel run all the tasks. We could also use ThreadPoolExecutor instead.
    s = time.time()
    tasks = []
    input_image_data = read_file(input_image_path)
    for index in range(100):
        output_image_path = os.path.join(output_image_dir, '{:>04}.png'.format(index))
        task = asyncio.create_task(write_image(output_image_path, input_image_data))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print('Cost: {} s'.format(time.time() - s))


if __name__ == '__main__':
    input_image_path = r"D:\tmp\image_input.png"
    output_image_dir = r"D:\tmp\image_export"
    main(input_image_path, output_image_dir)
    asyncio.run(basic_async_main(input_image_path, output_image_dir))
    asyncio.run(async_main(input_image_path, output_image_dir))
