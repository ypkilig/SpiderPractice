import scrapy
from SpiderPractice.items import AirLevelItem

class AirlevelSpider(scrapy.Spider):
    name = 'airlevel'
    allowed_domains = ['air-level.com']
    start_urls = ['https://www.air-level.com/']

    def parse(self, response):
        city_all = ["北京", "上海", "深圳", "广州"]
        cities =  response.xpath('//*[@id="citylist"]/div/a/text()').extract()
        node_urls = response.xpath('//*[@id="citylist"]/div/a/@href').extract()
        for city, url in zip(cities, node_urls):
            if city in city_all:
                url = response.urljoin(url)
                yield scrapy.Request(
                        url=url,
                        callback=self.airlevel_parse,
                        meta={'city':city}
                )

    def airlevel_parse(self, response):
        city = response.meta['city']
        time = response.xpath("//div[1]/div[3]/div[1]/div[1]/div/span[2]/text()").get()[:-2]
        tds = response.xpath("//table//tr[position()>1]")

        for td in tds:
            item = AirLevelItem()
            item["city"] = city
            item["time"] = time
            item["Stations"] = td.xpath("./td[1]/text()").get()
            item["Aqi"] = td.xpath("./td[2]/text()").get()
            item["level"] = td.xpath("./td[3]/span/text()").get()
            item["Pm25"] = td.xpath("./td[4]/text()").get()
            item["Pm10"] = td.xpath("/./td[5]/text()").get()
            item['Pripol'] = td.xpath("./td[6]/text()").get()
            print("城市：%s, 监测站：%s"%(item["city"], item["Stations"]))
            yield item
            

        