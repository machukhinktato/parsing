from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import requests


def int_maker(str_value):
    converter, result = [], []
    # str_value = ['1', '23', '4', '\\xa', '6', '7']
    for value in str_value:
        if value.isdecimal():
            converter.append(value)
    result = ''.join(converter)
    return int(result)


# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Python

# vacancy_pick = input('please, enter vacancy name: ').lower()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Safari/537.36',
}

params = {
    'area': '1',
    'fromSearchLine': 'true',
    'st': 'searchVacancy',
    'text': 'python',
    'from': 'suggest_post',
    # 'experience': 'noExperience',
}

resource = 'https://hh.ru'
req_params = '/search/vacancy'
response = requests.get(resource + req_params, params=params, headers=headers)
soup = bs(response.text, 'html.parser')

# for result in soup:
data_list = soup.findAll('div', {'class': 'vacancy-serp-item__row_header'})
salary, links, vacancy = [], [], []
for val in data_list:
    links.append(val.find('span').find('a').get('href'))
    vacancy.append(val.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text)
    compensation = val.findAll(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    # print(compensation)
    if compensation:
        for offered_sum in compensation:
            if 'руб' in offered_sum.text.lower():
                unit = 'руб'
                # print(offered_sum.text)
                for result in offered_sum:
                    if '-' in result:
                        result = result.split('-')
                        # for loop in range(len(result)):
                        start, end = int_maker(result[0]), int_maker(result[1][:-4])
                        # print(result)
                        print(f'{start}, {end}, {unit}')
                    elif 'от' in result:
                        start, end = int_maker(result[3:-4]), None
                        # print(f'{start}, {end}')
                    elif 'до' in result:
                        start, end = None, int_maker(result[3:-4])
                        start, end = None
            elif 'usd' in result:
                unit = 'usd'
            else:
                unit = 'eur'
            salary.append(offered_sum.text[-4:-1])
        else:
            salary.append(offered_sum.text[-3:])
else:
    salary.append(None)

pprint(len(salary))
pprint(len(links))
pprint(len(vacancy))
mega_list = {}
for i in range(len(vacancy)):
    mega_list.setdefault(vacancy[i], [salary[i], links[i]])
    # mega_list.append(vacancy[i])
    # mega_list.append(links[i])
    # mega_list.append(salary[i])

# pprint(mega_list)

# for i in endz:
#     int(i)
# a = ''.join(endz)
