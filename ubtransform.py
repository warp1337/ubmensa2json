# -*- coding: utf-8 -*-
import re
import sys
import json
import urllib2
from pprint import pprint
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

response = urllib2.urlopen('http://www.studentenwerkbielefeld.de/index.php?id=61')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

# These should be five, one day at a time
day_block_tables = soup.findAll("div", {"class": "day-block"})

# Menues for each day as list
menues = {"montag": [], "dienstag": [], "mittwoch": [], "donnerstag": [], "freitag": []}

# Well, these are the days
days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

# Collect special info about the "AT", since it may appear multiple times a day
special_case_aktions_theke = ""

idx = 0
for item in day_block_tables:
    # This is Monday to Friday
    for row in item.find_all('tr'):
        # Make this a function some day
        kind = str(row.find_all_next()[0].get_text().replace('/ Suppe', '').replace("\t", '').replace("\n", '')).replace('\xc3', 'u').replace('\xbc', 'e').replace('u\xa4', 'ae').replace('u\x9f', 'ss').replace('u\xb6', 'oe').lower().strip()
        food = str(row.find_all_next()[1].get_text().replace('/ Suppe', '').replace("\t", '').replace("\n", '')).replace('\xc3', 'u').replace('\xbc', 'e').replace('u\xa4', 'ae').replace('u\x9f', 'ss').replace('u\xb6', 'oe').lower().strip()
        # Ignore Dessert
        if "dessertbuffet" in kind:
            continue
        # Accumulate "Aktions-Theke", add at the end
        if kind == "aktions-theke":
            kind = "aktions theke"
            clean_food = re.sub(r'\(([^)]+)\)', '', food).replace("kcal", ". kcal").replace(".", ". ").replace("!", "! ").replace(":", ": ")
            special_case_aktions_theke += clean_food
            continue
        else:
            clean_food = re.sub(r'\(([^)]+)\)', '', food).replace("kcal", ". kcal").replace(".", ". ").replace("!", "! ").replace(":", ": ")
        if kind == "mensa vital":
            kind = "vital"
        if kind == "menue vegetarisch":
            kind = "vegetarisch"
        menues[days[idx]].append({kind: clean_food})
    # This one is a special case, add last
    menues[days[idx]].append({"aktions theke": special_case_aktions_theke})
    special_case_aktions_theke = ""
    idx += 1

with open('ub_mensa.json', 'w') as outfile:
    out = json.dumps(menues)
    outfile.write(out)
