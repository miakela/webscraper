import requests
from bs4 import BeautifulSoup
import json
from pandas import DataFrame as df
from tabulate import tabulate

page = requests.get("https://xoyondo.com/dp/MgcAgE04gPaVUf0/YLoiHW7Mgd")
soup = BeautifulSoup(page.text, 'html.parser')


months = []
days = []
people = []

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
removable = ["live-...", "m----...", "onlin..."] # needs to get ignored, dont know yet why they're shown, yet
for i in extr_people:
    if i.contents[0] not in removable:
        people.append(i.contents[0])

################################################################################
# formatting and printing table

table = [["Person1", "Yes"], ["Person2", "No"], ["Person3", "Maybe"]]
headers = [" "] + dates # empty slot in [0,0]
print(tabulate(table, headers, tablefmt='fancy_grid'))
