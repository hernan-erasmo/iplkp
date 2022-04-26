import json
import sys
from iplkp.lookup import lookup
from iplkp.consts import IPLKP_DESC
from iplkp.cache import IplkpCache, IplkpCacheException
import iplkp.utils as utils

def main():
    try:
        args = utils.parse_args(sys.argv)
    except utils.IplkpArgumentException as e:
        print(f"{e}")
        sys.exit(1)
    else:
        valid_addrs, invalid_addrs = utils.parse_address_args(args)

    if invalid_addrs:
        print(f"The following {len(invalid_addrs)} invalid IP addresses were found on input: {invalid_addrs}")

    if valid_addrs:
        print(f"Found {len(valid_addrs)} valid IP addresses on input: {valid_addrs}")
    else:
        print(f"No valid addresses found on input")
        sys.exit(1)

    if args.no_cache:
        results = lookup(valid_addrs, just_rdap=args.just_rdap, just_geo=args.just_geo)
    else:
        try:
            cache = IplkpCache()
        except IplkpCacheException as ex:
            print(f"{ex}. This is not an issue with iplkp. If the problem persists, try calling iplkp with --no-cache")
        cached_data, missing_IPs = cache.find_all(valid_addrs, just_rdap=args.just_rdap, just_geo=args.just_geo)
        if missing_IPs:
            results = lookup(missing_IPs, just_rdap=args.just_rdap, just_geo=args.just_geo)
            cache.update(results)
            for key in results.keys():
                results[key] |= cached_data[key]
        else:
            results = cached_data

    if args.save_output:
        with open(args.save_output, "w") as output:
            json.dump(results, output)
    sys.exit(0)
