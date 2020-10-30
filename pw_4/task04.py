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
        # check_dublicates = [i for i in db.find({})]
        if pub_link in [news_link.get('link') for news_link in db.find({})]:
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
    db, parsing_date = db_connection()
    link = 'https://yandex.ru/news/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']")
    for pub in news_block:
        # pub_data = {}
        pub_name = pub.xpath(".//h2/text()")
        pub_link = pub.xpath(".//h2/..//@href")
        publisher = pub.xpath(".//a/text()")
        pub_date = pub.xpath(".//span[@class='mg-card-source__time']/text()")
        # pprint(pub_link in [i.get('link') for i in check_dublicates])
        # pprint(pub_link in [print(i.get('link')) for i in db.find({})])
        # print(db_id)
        # print('https://yandex.ru/news/story/U_sovershivshego_napadenie_v_Nicce_nashli_Koran_i_nozh--d3f77e5a2061b2fb7b49055f70826853?lang=ru&rubric=index&wan=1&stid=e237g94J-SF38RIGuDt-&t=1604036779&tt=true&persistent_id=117629178' == 'https://yandex.ru/news/story/U_sovershivshego_napadenie_v_Nicce_nashli_Koran_i_nozh--d3f77e5a2061b2fb7b49055f70826853?lang=ru&rubric=index&wan=1&stid=e237-SF3g94J8RIGadgT&t=1604037226&tt=true&persistent_id=117629178' )
        # check_dublicates = [i for i in db.find({})]
        for elem in range(len(pub_name)):
            if pub_name[elem] in [news_name.get('name') for news_name in db.find({})]:
                continue
            else:

                # print(str(parsing_date.date()) + ' ' + pub_date[i])
                # print(pub_name[1])
                db_id = db.count_documents({})
                db.insert_one({
                    '_id': db_id + 1,
                    'name': pub_name[elem],
                    'date': str(parsing_date.date()) + ', ' + pub_date[elem],
                    'link': pub_link[elem],
                    'publisher': publisher[elem]
                })
                # test_list.append(pub_data)

        # print(dir(pub_name))
        # print(len(pub_name))
    # pprint(test_list)

    return pprint([i for i in db.find({})])

    # return pprint(news_block)


def mailru_check():
    db, parsing_date = db_connection()
    link = 'https://news.mail.ru/'
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)
    news_block = dom.xpath("//table[@class='daynews__inner']//td[position()<3]")
    # pprint(news_block)
    pub_data = {}
    for pub in news_block:
        # pub_data = {}
        pub_name = text_redactor(pub.xpath(".//span/text()"))
        pub_link = pub.xpath(".//a/@href")
        pub_date, publisher = None, None
        for news_link in pub_link:
            data_scrap = requests.get(news_link, headers=headers)
            link_dom = html.fromstring(data_scrap.text)
            # pub_date = link_dom.xpath("//div[@class='breadcrumbs breadcrumbs_article js-ago-wrapper']//span/@datetime")
            pub_date = link_dom.xpath("//span/@datetime")
            publisher = text_redactor(link_dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()"))
            # for elem in link_block:
            # pub_date = elem.xpath(".//span/@datetime")
        pub_data = {
            'name': pub_name,
            'date': pub_date,
            'link': pub_link,
            'publisher': publisher
        }
        # publisher = pub.xpath(".//a/text()")
        # pub_date = pub.xpath(".//span[@class='mg-card-source__time']/text()")
        # pprint(pub_link)


if __name__ == '__main__':
    # for i in
    # pprint(lenta_checker())
    # lentaru_check()
    # yandex_check()
    mailru_check()