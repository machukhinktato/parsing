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


def value_delimitter(compensation):
    first_val, second_val = None, None
    for result in compensation:
        if '-' in result:
            result = result.split('-')
            first_val, second_val = int_maker(result[0]), int_maker(result[1][:-4])
        elif 'от' in result:
            first_val, second_val = int_maker(result[3:-4]), None
        elif 'до' in result:
            first_val, second_val = None, int_maker(result[3:-4])
        else:
            continue
    return first_val, second_val


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
    start, end, unit = None, None, None
    all_cats = []
    if compensation:
        for offered_sum in compensation:
            # start, end, unit = None, None, None
            if 'руб' in offered_sum.text.lower():
                unit = 'руб'
                start, end = value_delimitter(offered_sum)
                # print(offered_sum.text)
                # for result in offered_sum:
                #     if '-' in result:
                #         result = result.split('-')
                # for loop in range(len(result)):
                # start, end = int_maker(result[0]), int_maker(result[1][:-4])
                # print(result)
                # print(f'{start}, {end}, {unit}')
                # elif 'от' in result:
                #     start, end = int_maker(result[3:-4]), None
                # print(f'{start}, {end}')
                # elif 'до' in result:
                #     start, end = None, int_maker(result[3:-4])
                # start, end = None
                all_cats.append(start)
                all_cats.append(end)
                all_cats.append(unit)
                salary.append(all_cats)
            elif 'usd' in offered_sum.text.lower():
                unit = 'usd'
                start, end = value_delimitter(offered_sum)
                all_cats.append(start)
                all_cats.append(end)
                all_cats.append(unit)
                salary.append(all_cats)
            else:
                unit = 'eur'
                start, end = value_delimitter(offered_sum)
                all_cats.append(start)
                all_cats.append(end)
                all_cats.append(unit)
                salary.append(all_cats)
    else:
        all_cats.append(start)
        all_cats.append(end)
        all_cats.append(unit)
        salary.append(all_cats)
        # salary.append(offered_sum.text[-4:-1])
    # else:
    #
    #     all_cats.append(start)
    #     all_cats.append(end)
    #     all_cats.append(unit)
    #     salary.append(all_cats)
# else:
#     salary.append(None)

pprint(len(salary))
pprint(len(links))
pprint(len(vacancy))
# mega_list = {}
# for i in range(len(vacancy)):
#     mega_list.setdefault(vacancy[i], [salary[i], links[i]])
# mega_list.append(vacancy[i])
# mega_list.append(links[i])
# mega_list.append(salary[i])

# pprint(mega_list)

# for i in endz:
#     int(i)
# a = ''.join(endz)
pprint(salary)
