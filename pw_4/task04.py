from lxml import html
from pymongo import MongoClient
from datetime import datetime as dt
from pprint import pprint
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Safari/537.36',
}


def db_connection():
    client = MongoClient('127.0.0.1', 27017)
    db = client['PW4']
    schema = db['news']
    parsing_date = dt.today()
    return schema, parsing_date


def text_redactor(data):
    return [txt.replace(u'\xa0', u' ') for txt in data]


def lentaru_check():
    db, parsing_data = db_connection()
    # db.delete_many({})  #turn on to clear database
    link = 'https://lenta.ru/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//time[@class='g-time']")
    for pub in news_block:
        pub_name = text_redactor(pub.xpath("./../text()"))
        pub_date = text_redactor(pub.xpath("./@datetime"))
        pub_link = link + pub.xpath("./../@href")[0]
        if pub_link in [news_link.get('link') for news_link in db.find({})]:
            continue
        else:
            db_id = db.count_documents({})
            db.insert_one({
                '_id': db_id + 1,
                'name': pub_name,
                'date': pub_date,
                'link': pub_link,
                'publisher': 'lenta.ru'
            })

    return pprint('lenta.ru scraping successfully done')


test_list = []


def yandex_check():
    db, parsing_date = db_connection()
    # db.delete_many({})  #turn on to clear database
    link = 'https://yandex.ru/news/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']")
    for pub in news_block:
        pub_name = pub.xpath(".//h2/text()")
        pub_link = pub.xpath(".//h2/..//@href")
        publisher = pub.xpath(".//a/text()")
        pub_date = pub.xpath(".//span[@class='mg-card-source__time']/text()")
        for elem in range(len(pub_name)):
            if pub_name[elem] in [news_name.get('name') for news_name in db.find({})]:
                continue
            else:
                db_id = db.count_documents({})
                db.insert_one({
                    '_id': db_id + 1,
                    'name': pub_name[elem],
                    'date': str(parsing_date.date()) + ', ' + pub_date[elem],
                    'link': pub_link[elem],
                    'publisher': publisher[elem]
                })

    return pprint('yandex.ru scraping successfully done')


def mailru_check():
    db, parsing_date = db_connection()
    # db.delete_many({})  #turn on to clear database
    link = 'https://news.mail.ru/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_links = dom.xpath("//a[contains(@class, 'js-topnews__item')]/@href")
    for news_link in news_links:
        request_data = requests.get(news_link, headers=headers)
        received_data = html.fromstring(request_data.text)
        pub_name = received_data.xpath("//h1/text()")
        pub_link = news_link
        pub_date = received_data.xpath("//span/@datetime")[0].split('+')
        publisher = received_data.xpath("//a[contains(@class, 'breadcrumbs')]/span/text()")
        if pub_link in [news_links.get('link') for news_links in db.find({})]:
            continue
        else:
            db_id = db.count_documents({})
            db.insert_one({
                '_id': db_id + 1,
                'name': pub_name,
                'date': pub_date[0].replace('T', ' '),
                'link': pub_link,
                'publisher': publisher
            })

    return pprint('mail.ru scraping successfully done')


def start_scraping():
    db, pd = db_connection()
    lentaru_check()
    yandex_check()
    mailru_check()

    return pprint([elem for elem in db.find({})])


if __name__ == '__main__':
    start_scraping()
