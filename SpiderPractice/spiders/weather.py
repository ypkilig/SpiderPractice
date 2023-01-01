import json
import scrapy
from lxml import etree
from urllib.parse import urlencode
from SpiderPractice.items import WeatherItem

class WeatherSpider(scrapy.Spider):

    name = 'weather'
    allowed_domains = ['2345.com']
    start_urls = ['https://tianqi.2345.com/']
    def parse(self, response):
        names_all = ["北京天气", "上海天气", "深圳天气", "广州天气"]
        names =  response.xpath('//*[@id="J_cityTq"]/div/a/text()').extract()
        node_urls = response.xpath('//*[@id="J_cityTq"]/div/a/@href').extract()
        for name, node_url in zip(names, node_urls):
            if name in names_all:
                yield scrapy.Request(
                        url=node_url,
                        callback=self.weaHistory_parse,
                        meta={'name':name}
                        )


    def weaHistory_parse(self, response):
        url_pre = "https://tianqi.2345.com/Pc/GetHistory"
        name = response.meta['name']
        year = 2022
        monthes = [i for i in range(1, 13)]
        areaId = response.url.split("/")[-1].split('.')[0]
        for month in monthes:
            params = {
                "areaInfo[areaId]": areaId,
                "areaInfo[areaType]":2,
                "date[year]":year,
                "date[month]":month,

            }
            params_str = urlencode(params)
            url = url_pre + "?" +params_str
            # url = self.start_urls[0] + '?' + params_str
            # url = f"https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D={areaId}&areaInfo%5BareaType%5D=2&date%5Byear%5D={year}&date%5Bmonth%5D={month}"
            yield scrapy.Request(
                    url=url,
                    callback=self.yearHistory_parse,
                    meta={'name':name}
                    )

    def yearHistory_parse(self, response):
        name = response.meta['name']
        res = json.loads(response.text)['data']
        tree = etree.HTML(res)
        dates = tree.xpath('//table/tr/td[1]/text()')
        Maxtempes = tree.xpath('//table/tr/td[2]/text()')
        Mintempes = tree.xpath('//table/tr/td[3]/text()')
        Weather = tree.xpath('//table/tr/td[4]/text()')
        Windir = tree.xpath('//table/tr/td[5]/text()')
        Aqi = tree.xpath('//table/tr/td//span/text()')
        for date,Maxtempe, Mintempe, Weather, Windir, Aqi in zip(dates, Maxtempes, Mintempes, Weather, Windir, Aqi):
            item = WeatherItem()
            item["name"] = name
            item["date"] = date
            item["Maxtempe"] = Maxtempe
            item["Mintempe"] = Mintempe
            item["Weather"] = Weather
            item["Windir"] = Windir
            item["Aqi"] = Aqi
            print("城市：%s, 日期：%s"%(item["name"], item["date"]))
            yield item
        