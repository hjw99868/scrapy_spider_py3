import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(scrapy.Spider):
	name = 'MySpider'

	allowed_domains = ['finance.sina.com.cn']

	start_urls = ['http://roll.finance.sina.com.cn/finance/zq1/zldx/index.shtml']

	def parse(self, response):
		try:
			for index in range(100):
				real_url = 'http://roll.finance.sina.com.cn/finance/zq1/zldx/index_' + str(index+2) + '.shtml'
				request = scrapy.Request(real_url, callback = self.parse_everytitle)
				yield request
		except:
			print("CRAWL OVER!!!!!")

	def parse_everytitle(self, response):
		for ul in range(8):
			for li in range(5):
				url_text = '//*[@id="Main"]/div[3]/ul[' + str(ul+1) + ']/li[' + str(li+1) + ']/a/@href'
				url = response.xpath(url_text).extract()
				print(url)
				request = scrapy.Request(url[0], callback = self.parse_everytext)
				yield request

	def parse_everytext(self, response):
		link = response.url
		text = response.xpath('//*[@id="artibody"]/p//text()').extract()
		strr = "".join(text)
		final_text = ''.join(strr.split())
		# final_text = ''
		# for line in f_text:  
		# 	final_text += str(line.strip())
		title = response.xpath('//*[@id="artibodyTitle"]/text()').extract()
		fo = open("artical.txt", 'a', encoding='utf-8')
		fo.write(link + " " + title[0] + " " + final_text + "\n") 