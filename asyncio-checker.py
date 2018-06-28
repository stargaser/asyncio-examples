import aiohttp
import asyncio
import json
import sys
import time


async def get_statuses(websites):
    statuses = {}
    async with aiohttp.ClientSession() as session:
        tasks = [get_website_status(session, website) for website in websites]
        for status in await asyncio.gather(*tasks):
            if not statuses.get(status):
                statuses[status] = 0
            statuses[status] += 1
    print(json.dumps(statuses))


async def get_website_status(session, url):
    async with session.get(url) as response:
        status = response.status
    return status


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = f.read().splitlines()
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_statuses(websites))
    t1 = time.time()
    print("getting website statuses took {0:.1f} seconds".format(t1-t0))
