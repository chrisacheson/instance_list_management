#!/usr/bin/env python3
"""
Merge the second CSV file into the first, and sort the result

"""
import csv
import sys


first_file = sys.argv[1]
second_file = sys.argv[2]
instances = dict()

with open(first_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    for row in reader:
        instances[row['hostname']] = row

with open(second_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        hostname = row['hostname']
        if hostname in instances:
            for field in fieldnames:
                if row[field] != "":
                    instances[hostname][field] = row[field]
        else:
            instances[hostname] = row

with open(first_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    hostnames = list(instances.keys())
    hostnames.sort()
    for hostname in hostnames:
        writer.writerow(instances[hostname])
