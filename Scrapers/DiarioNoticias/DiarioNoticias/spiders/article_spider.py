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

	name = "articles"

	start_urls = [
		'https://dn.pt/'
	]

	def __init__(self):
		self.driver = webdriver.Firefox(executable_path='/Users/PauloFrazao/Documents/Thesis/IdiomaFinal/Scrapers/DiarioNoticias/DiarioNoticias/geckodriver')

	def parse(self, response):

		for aside in response.css('aside.t-h-func-links ul'):
			for link in aside.css('li'):

				# extracts link of each heading
				link = link.css('::attr(href)').get()
				#print('Possible category:', link)

				# only follows heading if it is valid
				if link[0:5] != '/tag/':
					# or link != '/tag/cidades.html'
					#print('category scrapped :(')
					continue

				# constructs tag of each heading
				idx = link.find('.html')
				tag = link[5:idx]

				# follows each heading link
				newLink = 'https://dn.pt' + link
				
				yield SeleniumRequest(url=newLink, callback=self.parse_category)


	def parse_category(self, response):

		self.driver.get(response.url)

		for i in range(100):
			try:
				print('OJOEJOEFJ', i)
				if i != 0:
					try:
						actions = ActionChains(self.driver)
						last_height = self.driver.execute_script("return document.body.scrollHeight")
						self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
						actions.move_to_element(next).click().perform()
						next = self.driver.find_element_by_class_name('t-btn-8')
						#element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "t-btn-8"))).click()
					except Exception as e2:
						print("YOINKSSS")
						print(e2)
					#self.driver.execute_script("arguments[0].click();", next)
				else:
					next = self.driver.find_element_by_class_name('t-btn-8')
					next.click()
				time.sleep(15)
			except Exception as e:
				print(e)
				print('RUHROH')

		#resp = response.css('header.t-am-head')

		links = [i.get_attribute('href') for i in self.driver.find_elements_by_css_selector('.t-am-text')]
		print('fosforfjs', len(links))

		# for each potential link, ...
		for link in links:

			#print('potential link:', link)

			# discards links that link to tags
			if link[1:4] == 'tag':
				#print('link scrapped :(')
				continue

			# discards links without ids
			res = re.findall(r"\d{8}.html", link)
			if len(res) == 0:
				#print('link scrapped :(')
				continue

			# follows link if greater than prior count
			#newLink = 'https://dn.pt' + link 
			#print('final link:', newLink)
			yield scrapy.Request(link, self.parse_article)


	def parse_article(self, response):
		item = ArticleItem()
		item["link"] = response.url
		item["title"] = response.css('h1.t-af1-head-title::text').get()
		item["subtitle"] = response.css('div.t-af1-head-desc p::text').get()
		item["author"] = response.css('div.t-af-info-author span::text').get()
		item["date"] = response.css('div.t-af-info-1 time::text').get()
		# must figure out how to get the subheadings too!
		# must figure out how to get the pictures too!

		item["text"] = "" 
		for paragraph in response.css('div.t-af1-c1-body p::text').getall():
			item["text"] += paragraph

		item["tags"] = []
		for tag in response.css('nav.t-article-list-3-body ul li a span::text').getall():
			item["tags"].append(tag)
			#print(tag)
			#for nxt in tag.css('li').getall():
			#	for onemore in nxt.css('a::text'):
			#		item["tags"].append(onemore)

		return item