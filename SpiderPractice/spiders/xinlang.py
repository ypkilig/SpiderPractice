import scrapy
from urllib.parse import urlencode
from SpiderPractice.items import XinLangItem

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['vip.stock.finance.sina.com.cn']
    
    def start_requests(self):
        dev_url = 'https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml'
        page = 1
        parse = {
            "num":40,
            "p":page
        }
        url = dev_url + '?' + urlencode(parse)
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                "dev_url":dev_url,
                'parse':parse
            }
        )

    def parse(self, response):

        tds = response.xpath("//table[@id='dataTable']//tr[not(@style = 'display: none')]")

        for td in tds[1:]:
            item = XinLangItem()
            item["ID"] = td.xpath('./td[1]/a/text()').get()
            item["name"] = td.xpath("./td[2]/a/text()").get()
            item["count"] = td.xpath("./td[3]/text()").get()
            item["CoCh"] = td.xpath("./td[4]/text()").get()
            item["HoRatio"] = td.xpath("./td[5]/text()").get()
            item["InchoRatio"] = td.xpath("./td[6]/text()").get()
            item["PerTra"] = td.xpath("./td[7]/text()").get()
            item["InPerTra"] = td.xpath("./td[8]/text()").get()
            print("ID：%s, 名称：%s"%(item["ID"], item["name"]))
            yield item
        
        page_class = response.xpath('/html/body/div[1]/div[4]/div[2]/div/div[1]/div[5]/a[8]/@class').get()
        if page_class == 'page':
            dev_url = response.meta['dev_url']
            page = response.meta['parse']['p'] + 1
            parse = response.meta['parse']
            parse['p'] = page
            url = dev_url + '?' + urlencode(parse)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                "dev_url":dev_url,
                'parse':parse
            }
            )