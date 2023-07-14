#!/usr/bin/env python3
"""
Convert list of instances into CSV format. Assumed formatting:

    hostname divider description

The hostname can be with or without the protocol (https) part, optionally
followed by a trailing /
The divider consists of some combination of whitespace, commas, and hyphens.
If the description is a country/region, it will need to be manually moved to
the appropriate fields afterwards.

"""
import csv
import re
import sys


hostname_regex = re.compile(r"^([\w\.-]*)")
divider_regex = re.compile(r"^[\s,-]*")


writer = csv.DictWriter(sys.stdout, fieldnames=("hostname", "country",
                                                "region", "description"))
print("Paste text block to be converted, then press Ctrl+D:", file=sys.stderr)
text = sys.stdin.read()
writer.writeheader()
for line in text.splitlines():
    line = line.strip()
    if line == "":
        continue
    line = line.removeprefix("https://")
    _, hostname, line = hostname_regex.split(line, maxsplit=1)
    line = line.removeprefix("/")
    _, description = divider_regex.split(line, maxsplit=1)
    writer.writerow({"hostname": hostname, "description": description})
