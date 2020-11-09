import scrapy
from scrapy.http import HtmlResponse
from pw_6_scrapy_initial.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/' + target]
    target = 'search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
