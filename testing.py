# This file in so be deleted later
import re
import json

import requests
from bs4 import BeautifulSoup
from collections import defaultdict


valid_lecture = r'<tr><td>[0-9]</td><td>[0-9]{2}:[0-9]{2}<br/>[0-9]{2}:[0-9]{2}</td><td style=\"max-width: [0-9]{3}px;overflow: hidden;\">\(\w{1,3}\)<br.> [^<]{1,}<br/>[^td]{1,}td></tr>'
valid_time = r'<td>[0-9]{2}:[0-9]{2}<br/>[0-9]{2}:[0-9]{2}</td>'

payload = {
    'faculty': '1003',
    'course': '1',
    'group': 'КН-2201'.encode('cp1251'),
    'sdate': '01.04.2023',
    'edate': '30.04.2023',
}

data = requests.get('http://195.95.232.162:8082/cgi-bin/timetable.cgi', data=payload)

soup = BeautifulSoup(str(data.text).encode('ISO-8859-1'), 'lxml')

# print(soup.prettify())
# timetable = soup.find_all("table", {"class": "table"})[0].parent.parent.parent.find_all('tr')
# print(timetable)

stuff = soup.find_all("table", {"class": "table"})[0].parent.parent.parent.find_all('div', {'class': 'col-md-6'})
# print(stuff)

day = stuff[1]
timetable = day.find('table')


date = str(day.h4.find(string=True, recursive=False)).strip()

example_day = defaultdict(dict)
example_day[date]['day'] = day.h4.small.text
example_day[date]['lectures'] = {}

for lecture in timetable:
    match_string = re.search(valid_lecture, str(lecture))  # Makes sure lecture exists
    if match_string:
        lecture = match_string.group()
        lecture_soup = BeautifulSoup(lecture, 'lxml')  # Converts lecture string to BS object
        lecture_number = lecture_soup.td.text
        time_soup = lecture_soup.tr.td.findNext('td').text  # Extracts time of lecture from BS object
        example_day[date]['lectures'].setdefault(lecture_number, {})  # Prevents MissingKey error when adding to dictionary

        # Slices out time values from unified string
        lecture_start_time = time_soup[:5]
        lecture_end_time = time_soup[5:]

        # Merges those values into user-readable string and assigns them to dictionary
        lecture_time = f'{lecture_start_time} - {lecture_end_time}'
        example_day[date]['lectures'][lecture_number]['time'] = lecture_time

        lecture_type = str(lecture_soup).split('hidden;')[1][3:].split(')')[0]
        example_day[date]['lectures'][lecture_number]['type'] = lecture_type

        lecture_description = str(lecture_soup).split('<br/>')[2].replace(u'\xa0', ' ').strip()
        example_day[date]['lectures'][lecture_number]['description'] = lecture_description

        lecture_scale = str(lecture_soup).split('<br/>')[3].strip()
        example_day[date]['lectures'][lecture_number]['scale'] = lecture_scale


print(json.dumps(example_day, sort_keys=True, indent=4, ensure_ascii=False))

# for i in stuff:
#     print(i.h4.small.text)

# test_shit = re.findall('<tr><td>[0-9]</td><td>[0-9]{2}:[0-9]{2}<br/>[0-9]{2}:[0-9]{2}</td><td style=\"max-width: [0-9]{3}px;overflow: hidden;\">\(\w{1,3}\)<br.> [^<]{1,}<br/>[^td]{1,}td></tr>', str(soup.getText))

# print(test_shit)

# for i in test_shit:
#     print(i)