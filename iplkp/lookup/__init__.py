import asyncio
import time
from iplkp.lookup.geo_ip import geo_ip_lookup
from iplkp.lookup.rdap import rdap_lookup
from iplkp.consts import GEO_IP_LOOKUP_TASK_NAME, RDAP_LOOKUP_TASK_NAME
from iplkp.cache import IplkpCache, IplkpCacheException


async def run_queries(ip_list, just_rdap=False, just_geo=False):
    tasks = []
   
    query_all = not any([just_rdap, just_geo])

    if just_rdap or query_all:
        task_rdap = asyncio.create_task(rdap_lookup(ip_list), name=RDAP_LOOKUP_TASK_NAME)
        tasks.append(task_rdap)

    if just_geo or query_all:
        task_ip = asyncio.create_task(geo_ip_lookup(ip_list), name=GEO_IP_LOOKUP_TASK_NAME)
        tasks.append(task_ip)

    if tasks:
        await asyncio.gather(*tasks)
        return {task.get_name():task.result() for task in tasks}
    else:
        return {}


def lookup(ip_list, just_rdap=False, just_geo=False, use_cache=True):
    results = {}
    cache = None

    if use_cache:
        try:
            cache = IplkpCache()
        except IplkpCacheException as ex:
            print(f"{ex}. This is not an issue with iplkp. If the problem persists, try calling iplkp with --no-cache")
        else:
            cached_data, missing_IPs = cache.find_all(ip_list, just_rdap=just_rdap, just_geo=just_geo)
            if not missing_IPs:
                return cached_data
            else:
                ip_list = missing_IPs

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    time_start = time.time()
    results = asyncio.run(run_queries(ip_list, just_rdap=just_rdap, just_geo=just_geo))
    time_end = time.time()

    if cache and use_cache:
        cache.update(results)
        for key in results.keys():
            results[key] |= cached_data[key]

    print(f"Operation took {round(time_end - time_start, 1)} seconds")

    return results
