# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

response = urllib2.urlopen('http://www.studentenwerkbielefeld.de/index.php?id=61')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

# These should be five, one day at a time
day_block_tables = soup.findAll("div", {"class": "day-block"})

kind = []
menues = []

for item in day_block_tables:
    # This should be the kinds of food delivery
    for row in item.find_all('th'):
        kind.append(row.get_text().strip().replace("\t", '').replace("\n", ''))
    for row in item.find_all('td', {"class": "first"}):
        menues.append(row.get_text().strip().replace("\t", '').replace("\n", ''))

print len(kind)
print kind
print ""
print len(menues)
print menues
