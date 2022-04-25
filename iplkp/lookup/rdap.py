import asyncio
import aiohttp
from itertools import cycle
from iplkp.utils import show_remaining_tasks
from iplkp.consts import RDAP_CONNECTIONS_LIMIT, RDAP_CONNECTIONS_LIMIT_PER_HOST, RDAP_LOOKUP_TASK_PREFIX, IPLKP_EXCEPTION_KEY

RDAP_LOOKUP_ERROR_KEY = "iplkp_rdap_error"

RDAP_URLS = {
    'arin': 'http://rdap.arin.net/registry/ip/',
    'ripencc': 'http://rdap.db.ripe.net/ip/',
    'apnic': 'http://rdap.apnic.net/ip/',
    'lacnic': 'http://rdap.lacnic.net/rdap/ip/',
    'afrinic': 'http://rdap.afrinic.net/rdap/ip/'
}

def parse_rdap_lookup_content(ip, status, content):
    results = {}
    if status != 200:
        results[ip] = {
            RDAP_LOOKUP_ERROR_KEY: status,
            "message": "Error fetching RDAP info for the given IP"
        }
    else:
        results[ip] = content
    return results

async def fetch_rdap(url, ip, session):
    query_url = f"{url}{ip}"
    try:
        async with session.get(query_url) as response:
            show_remaining_tasks()
            content = await response.json()
            return parse_rdap_lookup_content(ip, response.status, content)
    except Exception as e:
        return {ip: {IPLKP_EXCEPTION_KEY: f"Exception while calling fetch_rdap: {repr(e)}"}}

async def rdap_lookup(ip_list):
    tasks = []
    rdap_urls = cycle(RDAP_URLS.values())
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=60)
    connector = aiohttp.TCPConnector(limit=RDAP_CONNECTIONS_LIMIT, limit_per_host=RDAP_CONNECTIONS_LIMIT_PER_HOST)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as rdap_session:
        for task_number, ip in enumerate(ip_list):
            url = next(rdap_urls)
            task = asyncio.create_task(fetch_rdap(url, ip, rdap_session), name=f"{RDAP_LOOKUP_TASK_PREFIX}{task_number}")
            tasks.append(task)
        task_results = await asyncio.gather(*tasks)
    responses = {}
    for t in task_results:
        responses |= t
    return responses
