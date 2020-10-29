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
    db = db_connection()
    # db.delete_many({})  #turn on to clear database
    link = 'https://lenta.ru/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//time[@class='g-time']")
    # data = dom.xpath("//div[@class='span4']//text()")
    # news_name = dom.xpath("./time[@class='g-time']/../text()")
    # news_name = news.
    # news_link = dom.xpath("//time[@class='g-time']/@datetime")
    # news_datepub = news.xpath("//@datetime")
    # return print([i.replace(u'\xa0', u' ') for i in news_link])
    # return pprint(news_name)
    # pub_name, pub_date = [], []
    news_data = []
    for pub in news_block:
        pub_data = {}
        # pb_name = pub.xpath("./../text()")
        # pub_name.append(text_redactor(pub.xpath("./../text()")))
        pub_name = text_redactor(pub.xpath("./../text()"))
        # pb_date = pub.xpath("./@datetime")
        # publication.append([txt.replace(u'\xa0', u' ') for txt in pb_name])
        # pub_date.append(text_redactor(pub.xpath("./@datetime")))
        pub_date = text_redactor(pub.xpath("./@datetime"))
        pub_link = link + pub.xpath("./../@href")[0]
        # for data in len(pub_name):
        db_id = db.count_documents({})
        check_dublicates = [i for i in db.find({})]
        if pub_link in [i.get('link') for i in check_dublicates]:
            continue
        else:
            db.insert_one({
                '_id': db_id + 1,
                'name': pub_name,
                'date': pub_date,
                'link': pub_link,
                'publisher': 'lenta.ru'
            })
        # pub_data = {
        #     'name': pub_name,
        #     'date': pub_date,
        #     'link': pub_link,
        #     'publisher': 'lenta.ru'
        # }
        # news_data.append(pub_data)
    # return pprint(news_data)
    return pprint([i for i in db.find({})])
    # return pprint(check_dublicates[0].get('link'))

test_list = []


def yandex_check():
    db = db_connection()
    link = 'https://yandex.ru/news/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']")
    for pub in news_block:
        pub_data = {}
        pub_name = pub.xpath(".//h2/text()")
        pub_link = pub.xpath(".//h2/..//@href")
        publisher = pub.xpath(".//a/text()")
        pub_date = pub.xpath(".//span[@class='mg-card-source__time']/text()")
        print(dir(pub_name))
        print(len(pub_name))
        # print(a = pub_name.count())
        for i in range(len(pub_name)):
        # print(pub_name[1])
            pub_data = {
                    'name': pub_name[i],
                    'date': pub_date[i],
                    'link': pub_link[i],
                    'publisher': publisher[i]
            }
            test_list.append(pub_data)
    pprint(dt.day)

    # return pprint(news_block)


if __name__ == '__main__':
    # for i in
    # pprint(lenta_checker())
    # lentaru_check()
    yandex_check()