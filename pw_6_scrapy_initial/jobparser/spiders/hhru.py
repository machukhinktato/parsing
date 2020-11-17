import scrapy
from scrapy.http import HtmlResponse
from pw_6_scrapy_initial.jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/' + target]
    # target = 'search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'
    target = 'search/vacancy?clusters=true&enable_snippets=true&text=python&L_save_area=true&area=1&from=cluster_area&showClusters=true'

    def parse(self, response:HtmlResponse):
        urls = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        for url in urls:
            yield response.follow(urls, callback=self.vacancy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p/span[@data-qa='bloko-header-2']/text()").extract()
        # link = response.xpath()
        # posted =


        yield JobparserItem(name=name, salary=salary)