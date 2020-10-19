from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import requests


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
    vacancy_pick = input('please, enter vacancy name: ').lower()

    params_hh = {
        'area': '1',
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': vacancy_pick,
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
            vac_desc_list.setdefault(vacancy[i], [salary[i], links[i]])
        if vac_desc_list:
            print(vac_desc_list)
            with open('task03.json', 'w', encoding='utf-8') as f:
                json.dump(vac_desc_list, f, indent=2, ensure_ascii=False)
        next_page = soup.find('a', {'data-qa': 'pager-next'})
        if next_page:
            params['page'] += 1
        else:
            break


def sj_parsing():
    sj_main_link = 'https://www.superjob.ru'
    sj_search_link = '/vacancy/search/'
    params = {
        'keywords': 'python',
        'geo': 'python',
        'page': '1',
    }
    # while True:
    response = requests.get(sj_main_link + sj_search_link, params=params, headers=headers)
    parsed_html = bs(response.text, 'html.parser')
    data_list = parsed_html.findAll('div', {'class': 'jNMYr GPKTZ _1tH7S'})
    # pprint(data_list)
    for i in data_list:
        pprint(i.find('a').text)

if __name__ == '__main__':
    # hh_parsing()
    sj_parsing()