import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def get_crawler(Spiders):
    settings = get_project_settings()
    crawler = CrawlerProcess(settings)
    for spider in Spiders:
        crawler.crawl(spider)
    return crawler


def main():
    Spiders = list(sys.argv)[1:]

    spidersList = os.popen('scrapy list')
    spidersList = spidersList.read().strip().split('\n')

    for spider in Spiders:
        if spider not in spidersList:
            print(f"不存在名为：{spider},爬虫列表仅有{spidersList}")
            sys.exit(2)

    crawler = get_crawler(Spiders=Spiders)
    crawler.start()

if __name__ == "__main__":
    main()
    





