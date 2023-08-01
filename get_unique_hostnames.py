#!/usr/bin/env python3
"""
Scan an arbitrary block of text for http/https URLs and extract, sort, and
deduplicate the hostnames. If big_list.csv or ignore.txt exist, any
hostnames in those will be removed from the final output.

"""
import csv
import re
import sys


hostname_regex = re.compile(r"https?://([\w\.-]+)")


print("Paste text block to be converted, then press Ctrl+D:", file=sys.stderr)
text = sys.stdin.read()
hostnames = hostname_regex.findall(text)
hostnames = map(lambda x: x.lower(), hostnames)
hostnames = set(hostnames)

try:
    with open("big_list.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            hostnames.discard(row["hostname"])
except IOError:
    pass

try:
    with open("ignore.txt") as ignore:
        for line in ignore:
            hostname = line.split("#", maxsplit=1)[0].strip()
            if hostname != "":
                hostnames.discard(hostname.lower())
except IOError:
    pass

hostnames = sorted(hostnames)
for hostname in hostnames:
    print(hostname)
