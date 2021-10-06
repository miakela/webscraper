import requests
from bs4 import BeautifulSoup
import json
from pandas import DataFrame as df
from tabulate import tabulate
import logging

page = requests.get("https://xoyondo.com/dp/MgcAgE04gPaVUf0/YLoiHW7Mgd")
soup = BeautifulSoup(page.text, 'html.parser')


months = []
days = []
people = []
ynm = []

################################################################################
# extracted dates

extr_months = soup.find_all(class_ = 'text-uppercase font-size-80 mt-1')
for i in extr_months:
    months.append(i.string)

extr_days = soup.find_all(class_ = 'font-size-120')
for i in extr_days:
    days.append(i.string)

# join days and months:
dates = [0]*(len(months))
for i in range(len(months)):
    dates[i] = days[i] + ". " + months[i]

################################################################################
# extracted people

extr_people = soup.find_all(class_ = 'name-abbrev-col-inner')
removable = ["live-...", "m----...", "onlin...", "Onlin..."] # needs to get ignored, dont know yet why they're shown, yet
for i in extr_people:
    if i.contents[0] not in removable:
        people.append(i.contents[0])
print(people)
################################################################################
# extracted votes = YesNoMaybe

removable_names = ["LIVE-ANGELIKA", "LIVE-MAIK", "M-----------------------------", "ONLINE- ZISKA", "ONLINE-ANGELIKA", "ONLINE-MAIK"]
for element in soup.find_all("tr"):
    for td in element.find_all("td"):
        try:
            if td['data-sort'] not in removable_names:
                ynm.append(td['data-sort'])
        except KeyError:
            pass
print(ynm)
################################################################################
# split vote list into multidim. list

votable = len(months) + 1
print(people)
votes = [[0 for x in range(votable)] for x in range(len(people))]

for j in range(len(people)):
    votes[j][0] = people[j] # people in first column
x = 0

# [j=row][i=column]
# fill in votes list with votings
for j in range(len(people)):
    x = 0
    for i in range(1, votable):
        votes[j][i] = ynm[i-1]
        x +=1
    del ynm[0:x]

################################################################################
# join people with votes
# votes = [[0]*(len(people))*(len(votable))]
# for columns in range(len(people)):
#     for rows in range(len(votable)):
#         votes[columns][rows] = people[columns]




################################################################################
# formatting and printing table

table = votes
# [["Person1", "Yes"], ["Person2", "No"], ["Person3", "Maybe"]]
headers = [" "] + dates # empty slot in [0,0]
print(tabulate(table, headers, tablefmt='fancy_grid'))

if __name__ == "__main__":
    logging.basicConfig(format= '%(message)s', filename="table", encoding='utf-8', level=logging.DEBUG)
    logging.info(tabulate(table, headers, tablefmt='fancy_grid'))
