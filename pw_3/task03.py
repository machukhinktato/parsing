from bs4 import BeautifulSoup as bs
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient
import json
import requests
import re

# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Python
# https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&page=2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Safari/537.36',
}


def sj_mongo_db():
    client = MongoClient('127.0.0.1', 27017)
    db = client['parsed_sj']
    vacancies = db['vacancies']
    return vacancies


def hh_mongo_db():
    client = MongoClient('127.0.0.1', 27017)
    db = client['parsed_hh']
    vacancies = db['vacancies']
    return vacancies


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


def hh_parsing():
    vacancies = hh_mongo_db()
    vac_desc_list = {}
    # vacancy_pick = input('please, enter vacancy name: ').lower()

    params_hh = {
        'area': '1',
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': 'python',
        'from': 'suggest_post',
        'experience': 'noExperience',
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
            # all_cats = []
            if compensation:
                for offered_sum in compensation:
                    start, end = value_delimitter(offered_sum)
                    if 'руб' in offered_sum.text.lower():
                        unit = 'руб'
                    elif 'usd' in offered_sum.text.lower():
                        unit = 'usd'
                    else:
                        unit = 'eur'
            # all_cats.append(start)
            # all_cats.append(end)
            # all_cats.append(unit)
            # salary.append(all_cats)
            salary.append([start, end, unit])
        #
        # for i in range(len(vacancy)):
        #     if vacancy[i] in vac_desc_list.keys():
        #         vacancy[i] = f'{vacancy[i]} - from {datetime.date()}'
        #     vac_desc_list.setdefault(vacancy[i], [salary[i], links[i]])
        #

        db_items = []
        for i in range(len(vacancy)):
            vac_desc_list.setdefault(i, [vacancy[i], salary[i], links[i]])
            id = vacancies.count_documents({})
            for data in vacancies.find({'url': links[i]}):
                db_items.append(data.get('url'))
            if links[i] in db_items:
                continue
            else:
                vacancies.insert_one({
                    '_id': id + 1,
                    'position': vacancy[i],
                    'from': salary[i][0],
                    'to': salary[i][1],
                    'unit': salary[i][2],
                    'url': links[i],
                })

                with open('task03_hh.json', 'w', encoding='utf-8') as f:
                    json.dump(vac_desc_list, f, indent=2, ensure_ascii=False)

        next_page = soup.find('a', {'data-qa': 'pager-next'})
        if next_page:
            params_hh['page'] += 1
        else:
            break


def sj_parsing():
    # db = client['parsed_sj']
    # vacancies = db['vacancies']
    vacancies = sj_mongo_db()
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
                    start = int(''.join([char for char in compensation.split('—')[0] if char.isdigit()]))
                    end = int(''.join([char for char in compensation.split('—')[1] if char.isdigit()]))
                    salary_list.append([start, end, unit])
                elif compensation.find('от') != -1:
                    start, end = int(''.join([char for char in compensation if char.isdigit()])), None
                    salary_list.append([start, end, unit])
                else:
                    start, end = None, int(''.join([char for char in compensation if char.isdigit()]))
                    salary_list.append([start, end, unit])

        db_items = []
        for i in range(len(vacancies_list)):
            vacancy_description.setdefault(i, [vacancies_list[i], salary_list[i], url_list[i]])
            id = vacancies.count_documents({})
            for vacancy in vacancies.find({'url': url_list[i]}):
                db_items.append(vacancy.get('url'))
            if url_list[i] in db_items:
                continue
            else:
                vacancies.insert_one({
                    '_id': id + 1,
                    'position': vacancies_list[i],
                    'from': salary_list[i][0],
                    'to': salary_list[i][1],
                    'unit': salary_list[i][2],
                    'url': url_list[i],
                })
                with open('task03_sj.json', 'w', encoding='utf-8') as f:
                    json.dump([i for i in vacancies.find()], f, indent=2, ensure_ascii=False)

        next_page = parsed_html.find('a', {'class': ['icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']})
        if next_page:
            params['page'] += 1
        else:
            break


# client = MongoClient('127.0.0.1', 27017)
# db = client['parsed_sj']
# vacancies = db['vacancies']
# with open('task03_sj.json', 'r', encoding='utf8') as file:
#     file_data = json.load(file)
#     # print(file_data)
# if isinstance(file_data, list):
#     for data in vacancies:
#         # print(data)
#         vacancies.insert_one(
#             {'_id': vacancies.value(),
#
#              }
#         )
# else:
#     vacancies.insert_one(file_data)
#


#
# client = MongoClient('127.0.0.1', 27017)

# for vac in vacancies.find({}):

def sj_db():
    vacancies = sj_mongo_db()
    # vacancies.delete_many({})
    for i in vacancies.find({}):
        print(i)


def hh_db():
    vacancies = hh_mongo_db()
    # vacancies.delete_many({})
    for i in vacancies.find({}):
        print(i)


if __name__ == '__main__':
    hh_parsing()
    hh_db()
    # sj_parsing()
    # sj_db()
