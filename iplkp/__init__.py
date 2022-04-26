import json
import sys
from iplkp.lookup import lookup
import iplkp.utils as utils

def main():
    try:
        args = utils.parse_args(sys.argv)
    except utils.IplkpArgumentException as e:
        print(f"{e}")
        sys.exit(1)
    else:
        valid_addrs = utils.parse_address_args(args)

    if not valid_addrs:
        sys.exit(1)

    results = lookup(valid_addrs, just_rdap=args.just_rdap, just_geo=args.just_geo, use_cache=args.use_cache)

    if args.save_output:
        with open(args.save_output, "w") as output:
            json.dump(results, output)
    else:
        print(results)
    sys.exit(0)
