#!/usr/bin/env python3
"""
Create markdown output from a CSV instance list

"""
from collections import defaultdict
import csv
from datetime import date
import sys


repo_url = "https://github.com/chrisacheson/instance_list_management"
md_indent = " " * 4


def make_instance_text(instance):
    hostname = instance["hostname"]
    url = f"https://{hostname}/"
    description = ""
    if instance["description"] != "":
        description = f" - {instance['description']}"
    return f"[{hostname}]({url}){description}"


instances_file = sys.argv[1]
topic_instances = list()
location_instances = defaultdict(lambda: defaultdict(list))

with open(instances_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        country = row["country"]
        if country == "":
            topic_instances.append(row)
        else:
            region = row["region"]
            location_instances[country][region].append(row)

countries = list(location_instances.keys())
countries.sort()

print(f"Updated {date.today().isoformat()}")
print()
print(f"A CSV version of this list is available at [{repo_url}]({repo_url})")
print()
print("Topic/audience focused:")
print()
for instance in topic_instances:
    print(f"- {make_instance_text(instance)}")
print()
print("Location/language focused:")
print()
print("(For some of these it's a little unclear to me whether they should be "
      "associated with a country or a language. Please let me know if "
      "anything needs to be corrected.)")
print()
for country in countries:
    country_regions = location_instances[country]
    if (
        len(country_regions) == 1 and
        "" in country_regions and
        len(country_regions[""]) == 1
    ):
        instance = country_regions[""][0]
        print(f"- {country} - {make_instance_text(instance)}")
    else:
        print(f"- {country}")
        regions = list(country_regions.keys())
        regions.sort()
        for region in regions:
            region_instances = country_regions[region]
            if len(region_instances) == 1:
                region_text = ""
                if region != "":
                    region_text = f"{region} - "
                instance = region_instances[0]
                instance_text = make_instance_text(instance)
                print(f"{md_indent}- {region_text}{instance_text}")
            else:
                if region != "":
                    print(f"{md_indent}- {region}")
                for instance in region_instances:
                    indent = md_indent
                    if region != "":
                        indent += md_indent
                    print(f"{indent}- {make_instance_text(instance)}")
