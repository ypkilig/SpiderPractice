import json
import scrapy
from urllib.parse import urlencode
from SpiderPractice.items import JdBook


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com']
    start_urls = ['https://book.jd.com/']

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        start_url = 'https://gw-e.jd.com/client.action?'
        category = "计算机与互联网"
        params = {
            "callback": "func",
            "body": {
                "moduleType":1,
                "page":1,
                "pageSize":20,
                "scopeType":1,
                "month":0,
                "categoryFirst":category
                },
            "functionId":"bookRank"
        }
        url = start_url + urlencode(params)
        meta = {
            "press_url" : start_url, 
            "params": params, 
        }
        yield scrapy.Request(url=url, dont_filter=True, meta=meta)

    def parse(self, response):
        params = response.meta['params']
        press_url = response.meta['press_url']
        data = json.loads(response.text[5:-1])["data"]
        books = data['books']
        page = params['body']['page']
        totalPage = data.get('totalPage')

        for id in range(len(books)):
            item = JdBook()
            book = books[id]
            item['bookName'] = book.get("bookName")
            for author in book.get("authors"):
                if  author['type'] == '译':
                    item['translator'] = author['name']
                else:
                    item['author'] = author['name']
            item['publisher'] = book.get('publisher')
            item['definePrice'] = book.get("definePrice")
            item["discount"] = book.get('discount')
            item['sellPrice'] = book.get('sellPrice')
            yield item
        
        if page < totalPage:
            params['body']['page'] = page + 1
            meta = response.meta
            meta['params']['page'] = page + 1
            url = press_url + urlencode(params)
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                meta=meta,
            )


