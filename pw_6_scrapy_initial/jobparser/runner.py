from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from pw_6_scrapy_initial.jobparser import settings
from pw_6_scrapy_initial.jobparser.spiders.hhru import HhruSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)

    process.start()
