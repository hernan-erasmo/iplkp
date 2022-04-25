import asyncio
import ipaddress
import re
from iplkp.consts import GEO_IP_LOOKUP_TASK_PREFIX, RDAP_LOOKUP_TASK_PREFIX


def show_remaining_tasks():
    def is_lookup_task(task):
        is_ip_lookup = task.get_name().startswith(GEO_IP_LOOKUP_TASK_PREFIX)
        is_rdap_lookup = task.get_name().startswith(RDAP_LOOKUP_TASK_PREFIX)
        return any([is_ip_lookup, is_rdap_lookup])
    remaining_tasks = len([t for t in asyncio.all_tasks() if is_lookup_task(t)])
    print(f"Remaining queries: {remaining_tasks}     \r", end="", flush=True)


def parse_address_args(args):
    addr_args = []
    valid_addrs = []
    invalid_addrs = []

    if args.ip_addr:
        addr_args.append(args.ip_addr)
    else:
        re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        try:
            with open(args.filename, "r") as ip_file:
                lines = ip_file.readlines()
        except (FileNotFoundError, OSError) as err:
            print(f"Couldn't read file {args.filename}: {str(err)}")
            return valid_addrs, invalid_addrs
        else:
            for line in lines:
                addr_args.extend(re.findall(re_ip, line))

    for addr in addr_args:
        try:
            valid_addrs.append(str(ipaddress.ip_address(addr)))
        except ValueError as ve:
            invalid_addrs.append(addr)
            continue

    return valid_addrs, invalid_addrs
