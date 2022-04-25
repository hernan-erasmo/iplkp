import asyncio
from iplkp.consts import GEO_IP_LOOKUP_TASK_PREFIX, RDAP_LOOKUP_TASK_PREFIX


def show_remaining_tasks():
    def is_lookup_task(task):
        is_ip_lookup = task.get_name().startswith(GEO_IP_LOOKUP_TASK_PREFIX)
        is_rdap_lookup = task.get_name().startswith(RDAP_LOOKUP_TASK_PREFIX)
        return any([is_ip_lookup, is_rdap_lookup])
    remaining_tasks = len([t for t in asyncio.all_tasks() if is_lookup_task(t)])
    print(f"Remaining queries: {remaining_tasks}     \r", end="", flush=True)
