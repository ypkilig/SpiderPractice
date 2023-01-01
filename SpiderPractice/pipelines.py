import csv
import os
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from SpiderPractice.items import MilockimgItem


class DownPipeline(object):

    def open_spider(self,spider):
        if spider.name != 'milockimg':
            path = f'./request/{spider.name}.csv'
            self.header = True
            self.f = open(path, 'w', encoding='utf-8', newline='')
                
    def process_item(self, item, spider):
        if spider.name != 'milockimg':
            req = dict(item)
            filedump = list(req.keys())
            writer = csv.DictWriter(self.f,fieldnames=filedump)
            if self.header:  
                writer.writeheader()
                self.header = False             
            writer.writerow(req)
        return item

    def close_spider(self, spider):  # 在爬虫关闭的时候仅执行一次
        if spider.name != 'milockimg':
            self.f.close()


class MiLockImagsPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, MilockimgItem):
            yield scrapy.Request(
                url=item['src'], 
                meta={
                    'title':item['title']
                }
            )

    def file_path(self, request, response=None, info=None):
        title = request.meta['title'].strip().replace(" ", "-")
        path = title + '.jpg'
        return path
    
    def item_completed(self, results, item, info):
        # 图片下载路径、url和校验和等信息
        
        return item