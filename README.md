# iplkp
[![PyPI version](https://badge.fury.io/py/iplkp.svg)](https://badge.fury.io/py/iplkp)

Geo IP and RDAP lookup command-line tool

## Description
**iplkp** is a command-line tool to fetch Geo IP and RDAP information about one or many IP addresses. It queries public URLs and API endpoints in order to fetch that information and either outputs it to the console or into a file for later analysis.

## Installation

    pip install iplkp

## Features

 - Asynchronous requests (through Aiohttp) allow querying information for many IP addresses while mitigating network wait time. 
 - Allows querying one or many IP addresses in a single run, either for RDAP, Geo IP information, or both.
 - Can take a file as input parameter and automatically extract all IP addresses from it's contents.
 - Caches queries by default, so it won't send requests for IP information already cached.


### Usage examples

    $ iplkp --ip-addres 8.8.8.8 --geo-ip

    {'ip_lookup': {'8.8.8.8': {'status': 'success', 'country': 'United States', 'countryCode': 'US', 'region': 'VA', 'regionName': 'Virginia', 'city': 'Ashburn', 'zip': '20149', 'lat': 39.03, 'lon': -77.5, 'timezone': 'America/New_York', 'isp': 'Google LLC', 'org': 'Google Public DNS', 'as': 'AS15169 Google LLC', 'query': '8.8.8.8'}}}

    $ iplkp --ip-addres 8.8.8.8 --rdap

    {'rdap_lookup': {'8.8.8.8': {'rdapConformance': ['nro_rdap_profile_0', 'rdap_level_0', 'cidr0', 'arin_originas0'], 'notices': [{'title': 'Terms of Service', 'description': ['By using the ARIN RDAP/Whois service, you are agreeing to the RDAP/Whois Terms of Use'], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'terms-of-service', 'type': 'text/html', 'href': 'https://www.arin.net/resources/registry/whois/tou/'}]}, {'title': 'Whois Inaccuracy Reporting', 'description': ['If you see inaccuracies in the results, please visit: '], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'inaccuracy-report', 'type': 'text/html', 'href': 'https://www.arin.net/resources/registry/whois/inaccuracy_reporting/'}]}, {'title': 'Copyright Notice', 'description': ['Copyright 1997-2022, American Registry for Internet Numbers, Ltd.']}], 'handle': 'NET-8-8-8-0-1', 'startAddress': '8.8.8.0', 'endAddress': '8.8.8.255', 'ipVersion': 'v4', 'name': 'LVLT-GOGL-8-8-8', 'type': 'ALLOCATION', 'parentHandle': 'NET-8-0-0-0-1', 'events': [{'eventAction': 'last changed', 'eventDate': '2014-03-14T16:52:05-04:00'}, {'eventAction': 'registration', 'eventDate': '2014-03-14T16:52:05-04:00'}], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'self', 'type': 'application/rdap+json', 'href': 'https://rdap.arin.net/registry/ip/8.8.8.0'}, {'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'alternate', 'type': 'application/xml', 'href': 'https://whois.arin.net/rest/net/NET-8-8-8-0-1'}, {'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'up', 'type': 'application/rdap+json', 'href': 'https://rdap.arin.net/registry/ip/8.0.0.0/9'}], 'entities': [{'handle': 'GOGL', 'vcardArray': ['vcard', [['version', {}, 'text', '4.0'], ['fn', {}, 'text', 'Google LLC'], ['adr', {'label': '1600 Amphitheatre Parkway\nMountain View\nCA\n94043\nUnited States'}, 'text', ['', '', '', '', '', '', '']], ['kind', {}, 'text', 'org']]], 'roles': ['registrant'], 'remarks': [{'title': 'Registration Comments', 'description': ['Please note that the recommended way to file abuse complaints are located in the following links. ', '', 'To report abuse and illegal activity: https://www.google.com/contact/', '', 'For legal requests: http://support.google.com/legal ', '', 'Regards, ', 'The Google Team']}], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'self', 'type': 'application/rdap+json', 'href': 'https://rdap.arin.net/registry/entity/GOGL'}, {'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'alternate', 'type': 'application/xml', 'href': 'https://whois.arin.net/rest/org/GOGL'}], 'events': [{'eventAction': 'last changed', 'eventDate': '2019-10-31T15:45:45-04:00'}, {'eventAction': 'registration', 'eventDate': '2000-03-30T00:00:00-05:00'}], 'entities': [{'handle': 'ABUSE5250-ARIN', 'vcardArray': ['vcard', [['version', {}, 'text', '4.0'], ['adr', {'label': '1600 Amphitheatre Parkway\nMountain View\nCA\n94043\nUnited States'}, 'text', ['', '', '', '', '', '', '']], ['fn', {}, 'text', 'Abuse'], ['org', {}, 'text', 'Abuse'], ['kind', {}, 'text', 'group'], ['email', {}, 'text', 'network-abuse@google.com'], ['tel', {'type': ['work', 'voice']}, 'text', '+1-650-253-0000']]], 'roles': ['abuse'], 'remarks': [{'title': 'Registration Comments', 'description': ['Please note that the recommended way to file abuse complaints are located in the following links.', '', 'To report abuse and illegal activity: https://www.google.com/contact/', '', 'For legal requests: http://support.google.com/legal ', '', 'Regards,', 'The Google Team']}, {'title': 'Unvalidated POC', 'description': ['ARIN has attempted to validate the data for this POC, but has received no response from the POC since 2019-10-24']}], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'self', 'type': 'application/rdap+json', 'href': 'https://rdap.arin.net/registry/entity/ABUSE5250-ARIN'}, {'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'alternate', 'type': 'application/xml', 'href': 'https://whois.arin.net/rest/poc/ABUSE5250-ARIN'}], 'events': [{'eventAction': 'last changed', 'eventDate': '2018-10-24T11:23:55-04:00'}, {'eventAction': 'registration', 'eventDate': '2015-11-06T15:36:35-05:00'}], 'port43': 'whois.arin.net', 'objectClassName': 'entity'}, {'handle': 'ZG39-ARIN', 'vcardArray': ['vcard', [['version', {}, 'text', '4.0'], ['adr', {'label': '1600 Amphitheatre Parkway\nMountain View\nCA\n94043\nUnited States'}, 'text', ['', '', '', '', '', '', '']], ['fn', {}, 'text', 'Google LLC'], ['org', {}, 'text', 'Google LLC'], ['kind', {}, 'text', 'group'], ['email', {}, 'text', 'arin-contact@google.com'], ['tel', {'type': ['work', 'voice']}, 'text', '+1-650-253-0000']]], 'roles': ['administrative', 'technical'], 'links': [{'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'self', 'type': 'application/rdap+json', 'href': 'https://rdap.arin.net/registry/entity/ZG39-ARIN'}, {'value': 'https://rdap.arin.net/registry/ip/8.8.8.8', 'rel': 'alternate', 'type': 'application/xml', 'href': 'https://whois.arin.net/rest/poc/ZG39-ARIN'}], 'events': [{'eventAction': 'last changed', 'eventDate': '2021-11-10T10:26:54-05:00'}, {'eventAction': 'registration', 'eventDate': '2000-11-30T13:54:08-05:00'}], 'status': ['validated'], 'port43': 'whois.arin.net', 'objectClassName': 'entity'}], 'port43': 'whois.arin.net', 'objectClassName': 'entity'}], 'port43': 'whois.arin.net', 'status': ['active'], 'objectClassName': 'ip network', 'cidr0_cidrs': [{'v4prefix': '8.8.8.0', 'length': 24}], 'arin_originas0_originautnums': []}}}

You can call it without specifying a particular query type, and it will return a JSON object with two keys: *ip_lookup* and *rdap_lookup*, each one of them with the queried IP(s) and their associated data.

### Options

    usage: iplkp [-h] (-i IP_ADDR | -b INPUT_FILE) [-g] [-r] [-o OUTPUT_FILE] [-f] [-c]
    
    iplkp - Geo IP and RDAP lookup tool
    
    optional arguments:
      -h, --help            show this help message and exit
      -i IP_ADDR, --ip-address IP_ADDR
                            Fetch information for a single given IP address
      -b INPUT_FILE, --bulk INPUT_FILE
                            Read IP addresses in bulk from INPUT_FILE
      -o OUTPUT_FILE, --output OUTPUT_FILE
                            Write output to a given OUTPUT_FILE
      -f, --force           Overwrite contents of OUTPUT_FILE if it exists
      -c, --no-cache        Do not use cache to fetch results. Do not update it after getting IP information
    
    Available queries:
      -g, --geo-ip          Only query Geo IP information for the given address or list of addresses
      -r, --rdap            Only query RDAP information for the given address or list of addresses

### Data sources

#### Geo IP
For Geo IP queries, iplkp uses the free version of https://ip-api.com/, particularly it's batch endpoint

    http://ip-api.com/batch

At the time of this writing, it had a rate limit of 15 calls every 60 seconds, and a batch of 100 IPs could be attached to each call. When given a list of IPs, **iplkp** automatically calculates the necessary rate to query the API in order to avoid going over the limit.

#### RDAP
Unfortunately I wasn't able to find a public API which would allow me to query RDAP information for IPs in bulk. The only way I could make **iplkp** get this data was to send HTTP requests to http://rdap.arin.net/registry/ip/. This didn't scale well, and after a while I noticed that ARIN would throttle if not drop requests altogether.
In order to mitigate this, **iplkp** implements a sort of Round Robin algorithm, which query different RDAP registries on each request, while also opening more than one connection to them in order to maximize throughput. RDAP information is currently queried from the following sources:

 - http://rdap.arin.net/registry/ip/ 
 - http://rdap.db.ripe.net/ip/ 
 - http://rdap.apnic.net/ip/ 
 - http://rdap.lacnic.net/rdap/ip/
 - http://rdap.afrinic.net/rdap/ip/

### Rate limits
While the API to query Geo IP data provides a clear indication of it's rate limits (which are pretty generous, allowing **iplkp** to query ~1500 IPs every 60 seconds), RDAP information providers are not explicit about their rate limits. 

**iplkp** is conservative in this sense, and aims to be a well-behaved tool, so it won't open many simultaneous connections to RDAP servers. Having said that, the author of this package has tried to query up to 5000  IPs simultaneously, and the whole operation took between 600 and 700 seconds. After that, heavy throttling was noticed.

## Tests
In order to run the unit tests, you must clone this repo first by doing

    $ git clone https://github.com/hernan-erasmo/iplkp.git

You'll probably want to setup a virtual environment in that directory. After that, just run

    $ python -m unittest -b
