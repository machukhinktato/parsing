from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import requests

# https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=Python

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Safari/537.36',
}

params = {

}

resource = 'https://hh.ru'
req_params = '/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
response = requests.get(resource + req_params, headers=headers)
dom = bs(response.text, 'html.parser')
abra_kadabra = dom.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})
print(len(abra_kadabra))
print(abra_kadabra)
