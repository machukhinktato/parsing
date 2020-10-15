from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import requests

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
    'from': 'suggest_post'
}

resource = 'https://hh.ru'
req_params = '/search/vacancy'
response = requests.get(resource + req_params, params=params, headers=headers)
soup = bs(response.text, 'html.parser')

for result in soup:
    compensation_list = soup.findAll('div', {'class': 'vacancy-serp-item__row_header'})
    vacancies_list = soup.findAll('a', {'data-qa': 'vacancy-serp__vacancy-title'})
# pprint(vacancies_list)
# soup.
pprint(compensation_list)
for val in compensation_list:
    # pprint(type(val))

    #как найти ссылку
    links = val.find('span').find('a').get('href')
    pprint(links)
    # pprint(type(i))
    # print(i.get('href'))
# worker_compensation, vacancy_name, links = [], [], []
# for compensation in compensation_list:
#     worker_compensation.append(compensation.text.lower())
# for vacancy in vacancies_list:
#     vacancy_name.append(vacancy.text.lower())
#     links.append(vacancy.get('href'))
# print(worker_compensation)
# print(vacancy_name)
# pprint(links)