# coding=utf-8

import json
import pandas
import gzip
from itertools import combinations
import pandas as pd

def parse_date(date):
    """
    Given a date in a format like:

    1 MAY 2016 - 00:30

    Return:

    2016-05-01
    """
    months = {"ene": "01", "feb": "02", "mar": "03", "abr": "04", "may": "05",
              "jun": "06", "jul": "07", "ago": "08", "sep": "09", "oct": "10",
              "nov": "11", "dic": "12"}

    pieces = date.lower().split(" ")
    new_date = pieces[2] + "-" + months[pieces[1]] + "-" + ("%02d" % int(pieces[0]))

    return(new_date)

def get_tag_pairs(tags):
    """Returns all the possible 2-tag combination"""
    tags = sorted([x.lower() for x in tags])
    return([x for x in combinations(tags, 2)])

if __name__ == "__main__":
    with gzip.open("/home/chema/Dropbox/data/cubazuela/elpais_opeds_full.json.gz", "r") as f:
        opeds = json.load(f)

    # Change dates and filter tags
    processed_opeds = []
    filter_tags = (u"opinión", )
    for oped in opeds:
        date = parse_date(oped["date"])
        tags = [x.lower() for x in oped["tags"] if x.lower() not in filter_tags]
        tag_pairs = get_tag_pairs(tags)
        for tag_pair in tag_pairs:
            processed_opeds.append({"date": date, "title": oped["title"], "url": oped["url"],
                                    "tag_pair_1": tag_pair[0], "tag_pair_2": tag_pair[1]})

    # Convert to Pandas object and dump to CSV file
    processed_opeds = pd.DataFrame(processed_opeds)
    processed_opeds.to_csv("/tmp/elpais_opeds.csv", index = False, encoding = "utf8")
