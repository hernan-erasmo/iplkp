import ipaddress
import re
import sys
import argparse
from iplkp.lookup import lookup
from iplkp.consts import IPLKP_DESC
import iplkp.utils as utils

def main():
    parser = argparse.ArgumentParser(description=IPLKP_DESC)
    main_group = parser.add_mutually_exclusive_group(required=True)
    main_group.add_argument("-i", "--ip-address", dest="ip_addr", metavar="IP_ADDR", help="Fetch information for a single given IP address")
    main_group.add_argument("-b", "--bulk", dest="filename", metavar="INPUT_FILE", help="Read IP addresses in bulk from INPUT_FILE")

    query_group = parser.add_argument_group(title="Available queries")
    query_group.add_argument("-g", "--geo-ip", dest="just_geo", help="Only query Geo IP information for the given address or list of addresses", action="store_true")
    query_group.add_argument("-r", "--rdap", dest="just_rdap", help="Only query RDAP information for the given address or list of addresses", action="store_true")

    parser.add_argument("-o", "--output", dest="save_output", metavar="OUTPUT_FILE", help="Write output to a given OUTPUT_FILE")
    parser.add_argument("-f", "--force", dest="overwrite", help="Overwrite contents of OUTPUT_FILE if it exists", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

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
