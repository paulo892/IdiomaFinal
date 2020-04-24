from __future__ import absolute_import
import scrapy
import re
import time
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class ArticleItem(scrapy.Item):
	link = scrapy.Field()
	title = scrapy.Field()
	subtitle = scrapy.Field()
	author = scrapy.Field()
	date = scrapy.Field()
	text = scrapy.Field()
	tags = scrapy.Field()

class ArticleSpider(scrapy.Spider):

	# spider name
	name = "articles"

	# url from which to start search
	start_urls = [
		'https://dn.pt/'
	]

	def __init__(self):
		# initializes Firefox webdriver for scraping
		self.driver = webdriver.Firefox(executable_path='/Users/PauloFrazao/Documents/Thesis/IdiomaFinal/Scrapers/DiarioNoticias/DiarioNoticias/geckodriver')

	def parse(self, response):
		# for each heading link...
		for aside in response.css('aside.t-h-func-links ul'):
			for link in aside.css('li'):

				# extracts link
				link = link.css('::attr(href)').get()

				# only follows link if it is "valid"
				if link[0:5] != '/tag/':
					continue

				# constructs tag for each heading
				idx = link.find('.html')
				tag = link[5:idx]

				# follows each heading link
				newLink = 'https://dn.pt' + link
				yield SeleniumRequest(url=newLink, callback=self.parse_category)


	def parse_category(self, response):
		# gets the response URL
		self.driver.get(response.url)

		# for 100 iterations...
		for i in range(100):
			try:
				# if not the first iteration...
				if i != 0:
					try:
						# scrolls to the bottom of the page and clicks "next page" button
						actions = ActionChains(self.driver)
						last_height = self.driver.execute_script("return document.body.scrollHeight")
						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						actions.move_to_element(next).click().perform()
						next = self.driver.find_element_by_class_name('t-btn-8')
					except Exception as e2:
						print(e2)
				# if first iteration...
				else:
					# finds and clicks "next page" button
					next = self.driver.find_element_by_class_name('t-btn-8')
					next.click()
				# waits for rest of page to load
				time.sleep(15)
			except Exception as e:
				print(e)

		# gets all of the links on the page
		links = [i.get_attribute('href') for i in self.driver.find_elements_by_css_selector('.t-am-text')]

		# for each link...
		for link in links:
			# discards if links to tags
			if link[1:4] == 'tag':
				continue

			# discards if has no IDs
			res = re.findall(r"\d{8}.html", link)
			if len(res) == 0:
				continue

			# follows link
			yield scrapy.Request(link, self.parse_article)

	def parse_article(self, response):
		# fills in "easy" article fields
		item = ArticleItem()
		item["link"] = response.url
		item["title"] = response.css('h1.t-af1-head-title::text').get()
		item["subtitle"] = response.css('div.t-af1-head-desc p::text').get()
		item["author"] = response.css('div.t-af-info-author span::text').get()
		item["date"] = response.css('div.t-af-info-1 time::text').get()

		# extracts text by adding each paragraph
		item["text"] = "" 
		for paragraph in response.css('div.t-af1-c1-body p::text').getall():
			item["text"] += paragraph

		# extracts each tag
		item["tags"] = []
		for tag in response.css('nav.t-article-list-3-body ul li a span::text').getall():
			item["tags"].append(tag)

		return item