import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import CivistabankItem
from itemloaders.processors import TakeFirst


class CivistabankSpider(scrapy.Spider):
	name = 'civistabank'
	start_urls = ['https://www.civista.bank/news-and-events']

	def parse(self, response):
		post_links = response.xpath('//a[@data-link-type-id="page"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="subpage-content1"]//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = re.findall(r'[A-Za-z]+\s\d{1,2},\s\d{4}', description) or ['']

		item = ItemLoader(item=CivistabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date[0])

		return item.load_item()
