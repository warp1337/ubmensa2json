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

menues = {"Montag": [], "Dienstag": [], "Mittwoch": [], "Donnerstag": [], "Freitag": []}
days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

idx = 0
for item in day_block_tables:
    # This is Monday to Friday
    for row in item.find_all('tr'):
        # Make this a function some day
        kind = str(row.find_all_next()[0].get_text().strip().replace("\t", '').replace("\n", '')).replace('\xc3', 'u').replace('\xbc', 'e').replace('u\xa4', 'ae').replace('u\x9f', 'ss').replace('u\xb6', 'oe')
        food = str(row.find_all_next()[1].get_text().strip().replace("\t", '').replace("\n", '')).replace('\xc3', 'u').replace('\xbc', 'e').replace('u\xa4', 'ae').replace('u\x9f', 'ss').replace('u\xb6', 'oe')
        if "Dessertbuffet" in kind:
            continue
        clean_food = re.sub(r'\(([^)]+)\)', '', food).replace("kcal", ". kcal")
        menues[days[idx]].append({kind: clean_food})
    idx += 1

with open('ub_mensa.json', 'w') as outfile:
    out = json.dumps(menues)
    outfile.write(out)
