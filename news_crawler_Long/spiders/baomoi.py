from dateutil import parser
import json
import os
import pandas as pd

import scrapy
from scrapy import Selector
from scrapy.http import Request, Response

class BaomoiSpider(scrapy.Spider):
    name = 'baomoi'
    # allowed_domains = ['https://baomoi.com/']
    based_url = 'https://baomoi.com'
    start_urls = []

    folder_path = "output/baomoi"

    categories = [
        'xa-hoi',
        'the-thao',
    ]
    categories_folder_path = {}
    categories_counter = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.page_limit = 5
        self.news_limit = 50
        
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        for category in self.categories:
            self.categories_counter[category] = [0, 0]

            path = self.folder_path + '/' + category
            self.categories_folder_path[category] = path
            if not os.path.exists(path):
                os.makedirs(path)

    def start_requests(self):
        for category in self.categories:
            url = f'{self.based_url}/{category}.epi'
            yield Request(
                url=url,
                callback=self.parse,
                meta={'category': category},
            )

    def parse(self, response: Response, **kwargs):
        category = response.meta.get('category')

        news_url_list = response.xpath('//div[@class="bm_OS bm_s"]//div[@class="bm_B"]//h4[@class="bm_G"]/span/a/@href').extract()

        for news_url in news_url_list[:2]:
            yield Request(
                self.based_url + news_url,
                callback=self.parse_news,
                meta={'category': category}
            )
            

    def parse_news(self, response: Response, **kwargs):
        category = response.meta.get('category')

        id = self.extract_id(response)
        datetime_data = self.extract_datetime(response)
        title = self.extract_title(response)
        abstract = self.extract_abstract(response)
        content = self.extract_content(response)

        value = {
            'id': id,
            'title': title,
            'datetime': datetime_data,
            'abstract': abstract,
            'content': content,
        }

        self.log(value)

        file_path = self.categories_folder_path[category] + '/' + id + '.json'
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(value, fp=fp, ensure_ascii=False)
            self.log(f'Saved file: {file_path}')

    def extract_id(self, response: Response):
        url: str = response.url
        elements = url.split('/')
        index = elements.index('c')
        return elements[index+1].replace('.epi', '')

    def extract_title(self, response: Response):
        title_data = response.xpath('//h1[@class="bm_G"]/text()').extract()[0]
        return title_data

    def extract_datetime(self, response: Response):
        datetime_data = response.xpath('//div[@class="bm_AL"]/time/@datetime').extract()[0]
        return datetime_data

    def extract_abstract(self, response: Response):
        abstract_data = response.xpath('//h3[@class="bm_y bm_G"]/text()').extract()[0]
        return abstract_data

    def extract_content(self, response: Response):
        content_data =  response.xpath('//div[@class="bm_IM"]/p[@class="bm_BI"]/text()').extract()
        return '\n'.join(content_data)