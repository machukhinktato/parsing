from bs4 import BeautifulSoup as bs
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient
import json
import requests
import re


def int_maker(str_value):
    converter, result = [], []
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
# https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&page=2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Safari/537.36',
}


def hh_parsing():
    vac_desc_list = {}
    # vacancy_pick = input('please, enter vacancy name: ').lower()

    params_hh = {
        'area': '1',
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': 'python',
        'from': 'suggest_post',
        # 'experience': 'noExperience',
        'page': 0,
    }

    resource = 'https://hh.ru'
    continued_link = '/search/vacancy'
    while True:
        response = requests.get(resource + continued_link, params=params_hh, headers=headers)
        soup = bs(response.text, 'html.parser')
        data_list = soup.findAll('div', {'class': 'vacancy-serp-item__row_header'})
        salary, links, vacancy = [], [], []
        for val in data_list:
            links.append(val.find('span').find('a').get('href'))
            vacancy.append(val.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text)
            compensation = val.findAll(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            start, end, unit = None, None, None
            all_cats = []
            if compensation:
                for offered_sum in compensation:
                    start, end = value_delimitter(offered_sum)
                    if 'руб' in offered_sum.text.lower():
                        unit = 'руб'
                    elif 'usd' in offered_sum.text.lower():
                        unit = 'usd'
                    else:
                        unit = 'eur'
            all_cats.append(start)
            all_cats.append(end)
            all_cats.append(unit)
            salary.append(all_cats)

        for i in range(len(vacancy)):
            if vacancy[i] in vac_desc_list.keys():
                vacancy[i] = f'{vacancy[i]} - from {datetime.date()}'
            vac_desc_list.setdefault(vacancy[i], [salary[i], links[i]])

        # vac_data.insert_many(vac_desc_list)

        if vac_desc_list:
            print(vac_desc_list)
            with open('task03_hh.json', 'w', encoding='utf-8') as f:
                json.dump(vac_desc_list, f, indent=2, ensure_ascii=False)
        next_page = soup.find('a', {'data-qa': 'pager-next'})
        if next_page:
            params_hh['page'] += 1
        else:
            return vac_desc_list
            break


def sj_parsing():
    sj_main_link = 'https://www.superjob.ru'
    sj_search_link = '/vacancy/search/'
    params = {
        'keywords': 'python',
        'geo': 'python',
        'page': 0,
    }
    vacancy_description = {}
    while True:
        response = requests.get(sj_main_link + sj_search_link, params=params, headers=headers)
        parsed_html = bs(response.text, 'html.parser')
        data_list = parsed_html.findAll('div', {'class': 'jNMYr GPKTZ _1tH7S'})
        vacancies_list, salary_list, url_list, compensation_list = [], [], [], []
        for data in data_list:
            vacancies_list.append(data.find('a').text)
            compensation_list.append(data.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).text)
            url_route = data.find('a').get('href')
            url_list.append(sj_main_link + url_route)
        if compensation_list:
            for compensation in compensation_list:
                if 'руб' in compensation:
                    unit = 'руб'
                elif 'usd' in compensation:
                    unit = 'usd'
                elif 'eur' in compensation:
                    unit = 'eur'
                else:
                    start, end, unit = None, None, None
                    salary_list.append([start, end, unit])
                    continue

                if compensation.find('—') != -1:
                    start = ''.join([char for char in compensation.split('—')[0] if char.isdigit()])
                    end = ''.join([char for char in compensation.split('—')[1] if char.isdigit()])
                    salary_list.append([start, end, unit])
                elif compensation.find('от') != -1:
                    start, end = ''.join([char for char in compensation if char.isdigit()]), None
                    salary_list.append([start, end, unit])
                else:
                    start, end = None, ''.join([char for char in compensation if char.isdigit()])
                    salary_list.append([start, end, unit])

        for i in range(len(vacancies_list)):
            # if vacancies_list[i] in vacancy_description.keys():
            #     vacancies_list[i] = f'{vacancies_list[i]} - from {datetime.hour}'
            vacancy_description.setdefault(i, [vacancies_list[i], salary_list[i], url_list[i]])
        if vacancy_description:
            with open('task03_sj.json', 'w', encoding='utf-8') as f:
                json.dump(vacancy_description, f, indent=2, ensure_ascii=False)
        next_page = parsed_html.find('a', {'class': ['icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']})
        if next_page:
            params['page'] += 1
        else:
            return vacancy_description
            break



client = MongoClient('127.0.0.1', 27017)
db = client['parsed_hh']
vacancies = db['vacancies']
with open('task03_sj.json', 'r', encoding='utf8') as file:
    file_data = json.load(file)
    # print(file_data)
if isinstance(file_data, list):
    vacancies.insert_many(file_data)
else:
    vacancies.insert_one(file_data)


for vac in vacancies.find({}):
    pprint(vac)

if __name__ == '__main__':
    # hh_parsing()
    sj_parsing()
