import requests
from bs4 import BeautifulSoup
import json
from pandas import DataFrame as df
from tabulate import tabulate
import sys

page = requests.get("https://xoyondo.com/dp/MgcAgE04gPaVUf0/YLoiHW7Mgd")
soup = BeautifulSoup(page.text, 'html.parser')


people = []
months_count = 0
months = []

################################################################################
# extracted dates

extr_months = soup.find_all(class_ = 'text-uppercase font-size-80 mt-1')
for i in extr_months:
    months.append(i.string)
    months_count += 1

rows = len(months)
col = 2
date = [[0]*rows]*col

days = []
extr_days = soup.find_all(class_ = 'font-size-120')
for i in extr_days:
    days.append(i.string)


# output should be: [[08, Oktober], [09, Oktober]]
for i in range(21):
    for j in range(1):
        date[j][i] = [days[i],months[i]]
#print("_______________________________________________________")
#print(date) # multidimensional list

################################################################################
# extracted people
people_extr = soup.find_all(class_ = 'name-abbrev-col-inner')
removable = ["live-...", "m----...", "onlin..."] # needs to get ignored, dont know yet why there shown
for i in people_extr:
    if i.contents[0] not in removable:
        people.append(i.contents[0])

################################################################################

print(people)
table = [people, date]
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
