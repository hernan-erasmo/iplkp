import re
import sys
import argparse

DESC = "iplkp - Geo IP and RDAP lookup tool"

def main():
    parser = argparse.ArgumentParser(description=DESC)
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

    addr_args = []

    if args.ip_addr:
        addr_args.append(args.ip_addr)
    else:
        re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        try:
            with open(args.filename, "r") as ip_file:
                lines = ip_file.readlines()
        except (FileNotFoundError, OSError) as err:
            print(f"Couldn't read file {args.filename}: {str(err)}")
            sys.exit(1)
        else:
            for line in lines:
                addr_args.extend(re.findall(re_ip, line))
