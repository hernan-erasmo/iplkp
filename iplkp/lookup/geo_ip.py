import asyncio
import json
import aiohttp
from iplkp.utils import show_remaining_tasks
from iplkp.consts import GEO_IP_LOOKUP_TASK_PREFIX, IPLKP_EXCEPTION_KEY

GEO_IP_LOOKUP_ERROR_KEY = "iplkp_geo_ip_error"

# API provider for IP Geolocation queries: http://ip-api.com
IP_URL = "http://ip-api.com/batch"
# API says max is 15 every 60 seconds, which translates to 1 every 4 seconds.
# Using 5 just to be extra cautious.
SECONDS_BETWEEN_REQUESTS = 5
MAX_IPS_PER_BATCH = 100


def generate_buckets(lst, bucket_size):
    """Yield successive n-sized buckets from lst"""
    for i in range(0, len(lst), bucket_size):
        yield lst[i:i + bucket_size]

def parse_ip_lookup_content(content):
    results = {}
    for elem in content:
        query = elem["query"]
        status = elem["status"]

        if status != "success":
            results[query] = {
                GEO_IP_LOOKUP_ERROR_KEY: status,
                "message": elem["message"]
            }
        else:
            results[query] = elem
    return results

async def fetch_ip_batch(ip_bucket, delay, session):
    # hack to avoid having to deal with the API's rate limit dynamically.
    # We just schedule the requests at a rate that will never go over the limit
    await asyncio.sleep(delay)

    try:
        async with session.post(IP_URL, data=json.dumps(ip_bucket)) as response:
            show_remaining_tasks()
            content = await response.json()
            return parse_ip_lookup_content(content)
    except Exception as exception:
        return {IPLKP_EXCEPTION_KEY: f"Exception while calling fetch_ip_batch: {repr(exception)}"}

async def geo_ip_lookup(ip_list):
    tasks = []
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=15)
    connector = aiohttp.TCPConnector(limit=1, limit_per_host=1, force_close=True)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as ip_session:
        delay = 0
        for task_number, ip_bucket in enumerate(generate_buckets(ip_list, MAX_IPS_PER_BATCH)):
            task = asyncio.create_task(
                fetch_ip_batch(ip_bucket, delay, ip_session), name=f"{GEO_IP_LOOKUP_TASK_PREFIX}{task_number}")
            delay += SECONDS_BETWEEN_REQUESTS
            tasks.append(task)
        task_results = await asyncio.gather(*tasks)
    responses = {}
    for result in task_results:
        responses |= result
    return responses
