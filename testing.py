# This file in so be deleted later


import requests
from bs4 import BeautifulSoup

payload = {
    'n': '700',
    'faculty': '1003',
    'course': '1',
    'group': 'КН-2201'.encode('cp1251')
}

data = requests.get('http://195.95.232.162:8082/cgi-bin/timetable.cgi', data=payload)

soup = BeautifulSoup(str(data.text).encode('ISO-8859-1'), 'lxml')

# print(soup.prettify())
timetable = soup.find_all("table", {"class": "table"})[0].parent.parent.parent.find_all('tr')

for i in timetable:
    print(i)