# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    name = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()
    Maxtempe = scrapy.Field()
    Mintempe = scrapy.Field()
    Weather = scrapy.Field()
    Windir = scrapy.Field()
    Aqi = scrapy.Field()

class AirLevelItem(scrapy.Item):
    city = scrapy.Field()
    time = scrapy.Field()
    Stations = scrapy.Field()
    Aqi = scrapy.Field()
    level = scrapy.Field()
    Pm25 = scrapy.Field()
    Pm10 = scrapy.Field()
    Pripol = scrapy.Field()

class MilockimgItem(scrapy.Item):
    title = scrapy.Field()
    src = scrapy.Field()

class XinLangItem(scrapy.Item):
    ID = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    CoCh = scrapy.Field()
    HoRatio = scrapy.Field()
    InchoRatio = scrapy.Field()
    PerTra = scrapy.Field()
    InPerTra = scrapy.Field()

class JdBook(scrapy.Item):
    bookName = scrapy.Field()
    author = scrapy.Field()
    translator = scrapy.Field()
    publisher = scrapy.Field()
    definePrice = scrapy.Field()
    discount = scrapy.Field()
    sellPrice = scrapy.Field()
    