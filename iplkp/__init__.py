import sys
from iplkp.lookup import lookup
from iplkp.consts import IPLKP_DESC
import iplkp.utils as utils

def main():
    if not (args := utils.parse_args(sys.argv)):
        print(f"Missing required arguments")
        sys.exit(1)

    valid_addrs, invalid_addrs = utils.parse_address_args(args)

    if invalid_addrs:
        print(f"The following {len(invalid_addrs)} invalid IP addresses were found on input: {invalid_addrs}")

    if valid_addrs:
        print(f"Found {len(valid_addrs)} valid IP addresses on input: {valid_addrs}")
    else:
        print(f"No valid addresses found on input")
        sys.exit(1)

    # TODO: caching begins here, removing addresses in cache from valid_addrs.
    results = lookup(valid_addrs, just_rdap=args.just_rdap, just_geo=args.just_geo)
    # TODO: caching ends here
    #   TODO: injecting cached IPs into results.
    #   TODO: saving new results

    print(results)
    sys.exit(0)
