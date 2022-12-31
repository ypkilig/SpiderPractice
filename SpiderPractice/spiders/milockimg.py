import scrapy
from SpiderPractice.items import MilockimgItem

class MilockimgSpider(scrapy.Spider):
    name = 'milockimg'
    allowed_domains = ['xiaomi.com']
    start_urls = ['http://zhuti.xiaomi.com/lockstyle']

    def parse(self, response):
        node_url = response.xpath('//*[@id="main"]/div/div[1]/div[1]/a/@href').extract_first()
        url = response.urljoin(node_url)
        yield scrapy.Request(
            url=url,
            callback=self.locksrc_parse
        )

    def locksrc_parse(self, response):
        title = response.xpath("//*[@id='main']//div[@class='bd']/ul/li/div/a/b/img/@alt").extract()
        src = response.xpath("//*[@id='main']/div/div[1]/div[2]/ul/li/div[1]/a/@href").extract()


        for title, url in zip(title, src):
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url,
                callback=self.lockimg_parse,
                meta={"title":title}
            )
        
        part_url  = response.xpath("//*[@id='main']/div/div[2]/div/a[last()]/@href").extract_first()
        part_name = response.xpath("//*[@id='main']/div/div[2]/div/a[last()]/text()").extract_first()

        if part_name == '下一页':
            url = response.urljoin(part_url)
            yield scrapy.Request(
                url=url,
                callback=self.locksrc_parse
            )

    def lockimg_parse(self,response):
        title = response.meta["title"]
        src = response.xpath('//*[@id="J_detail"]/div/img/@src').extract_first()
        item = MilockimgItem()
        item['title'] = title
        item["src"] = src
        print(title.strip().replace(" ", "-") + '.jpg')
        yield item
