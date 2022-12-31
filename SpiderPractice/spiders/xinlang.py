import scrapy
from SpiderPractice.items import XinLangItem

class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['vip.stock.finance.sina.com.cn']
    start_urls = ['https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml?num=40&p=1']

    def parse(self, response):
        ID = response.xpath("//*[@id='dataTable']//tr//td[1]/a/text()").extract()
        name = response.xpath("//*[@id='dataTable']//tr//td[2]/a/text()").extract()
        count = response.xpath("//*[@id='dataTable']//tr//td[3]/text()").extract()
        CoCh = response.xpath("//*[@id='dataTable']//tr//td[4]/text()").extract()
        HoRatio = response.xpath("//*[@id='dataTable']//tr//td[5]/text()").extract()
        InchoRatio = response.xpath("//*[@id='dataTable']//tr//td[6]/text()").extract()
        PerTra = response.xpath("//*[@id='dataTable']//tr//td[7]/text()").extract()
        InPerTra = response.xpath("//*[@id='dataTable']//tr//td[8]/text()").extract()
        for i in range(len(name)):
            item = XinLangItem()
            item["ID"] = ID[i]
            item["name"] = name[i]
            item["count"] = count[i]
            item["CoCh"] = CoCh[i]
            item["HoRatio"] = HoRatio[i]
            item["InchoRatio"] = InchoRatio[i]
            item["PerTra"] = PerTra[i]
            item["InPerTra"] = InPerTra[i]
            print("ID：%s, 名称：%s"%(item["ID"], item["name"]))
            yield item
        
        page = int(response.url.split('=')[-1]) + 1
        page_class = response.xpath('/html/body/div[1]/div[4]/div[2]/div/div[1]/div[5]/a[8]/@class').extract_first()
        if page_class == 'page':
            next_url = f"https://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/jgcg/index.phtml?num=40&p={page}"
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )