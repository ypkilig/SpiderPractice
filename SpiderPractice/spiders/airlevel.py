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
        time = response.xpath("//div[1]/div[3]/div[1]/div[1]/div/span[2]/text()").extract_first()[:-2]
        Stations = response.xpath("//table//tr/td[1]/text()").extract()
        Aqi = response.xpath("//table//tr/td[2]/text()").extract()
        level = response.xpath("//table//tr/td[3]/span/text()").extract()
        Pm25 = response.xpath("//table//tr/td[4]/text()").extract()
        Pm10 = response.xpath("//table//tr/td[5]/text()").extract()
        Pripol = response.xpath("//table//tr/td[6]/text()").extract()
        for i in range(len(Stations)):
            item = AirLevelItem()
            item["city"] = city
            item["time"] = time
            item["Stations"] = Stations[i]
            item["Aqi"] = Aqi[i]
            item["level"] = level[i]
            item["Pm25"] = Pm25[i]
            item["Pm10"] = Pm10[i]
            if i < len(Pripol):
                item["Pripol"] = Pripol[i]
            print("城市：%s, 监测站：%s"%(item["city"], item["Stations"]))
            yield item

        #for Stations, Aqi, level, Pm25, Pm10,Pripol in zip(Stations, Aqi, level, Pm25, Pm10, Pripol):
            

        