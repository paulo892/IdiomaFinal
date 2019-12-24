import scrapy

class ArticleItem(scrapy.Item):
	link = scrapy.Field()
	title = scrapy.Field()
	subtitle = scrapy.Field()
	author = scrapy.Field()
	date = scrapy.Field()
	text = scrapy.Field()
	tags = scrapy.Field()

class ArticlesSpider(scrapy.Spider):

	name = "articles"

	start_urls = [
		'https://elpais.com/',
		#'https://elpais.com/tag/oriente_proximo/'
	]

	def parse(self, response):
		for name in response.css('ul.seccion-submenu-navegacion-listado li'):
			link = name.css('a::attr(href)').get()
			yield response.follow(link, callback=self.parse_field)

	def parse_field(self, response):
		for name in response.css('ul.seccion-submenu-navegacion-listado li'):
			link = name.css('a::attr(href)').get()
			yield response.follow(link, callback=self.parse_subfield)

	def parse_subfield(self, response):
		for article in response.css('h2.articulo-titulo'):
			link = article.css('a::attr(href)').get()
			yield response.follow(link, callback=self.parse_article)

		link_next = response.css('li.paginacion-siguiente a::attr(href)').get()
		yield response.follow(link_next, callback=self.parse_subfield)

	def parse_article(self, response):
		item = ArticleItem()
		item["link"] = response.url
		item["title"] = response.css('h1.articulo-titulo::text').get()
		item["subtitle"] = response.css('h2.articulo-subtitulo::text').get()
		item["author"] = response.css('span.autor-nombre a::text').get()
		item["date"] = response.css('time.articulo-actualizado a::text').get()
		# must figure out how to get the subheadings too!
		# must figure out how to get the pictures too!

		item["text"] = "" 
		for paragraph in response.css('div.articulo__contenedor p::text').getall():
			item["text"] += paragraph

		item["tags"] = []
		for tag in response.css('div.articulo-tags__interior ul.listado li a::text').getall():
			item["tags"].append(tag)

		
		return item




		#for name in response.css('ul.seccion-submenu-navegacion-listado li'):
		#	yield {
		#		'temp': name.css('a::attr(href)').get()
		#	}