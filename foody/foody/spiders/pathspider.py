import scrapy


class PathspiderSpider(scrapy.Spider):
    name = "pathspider"
    allowed_domains = ["www.foody.vn"]
    start_urls = ["https://www.foody.vn/"]

    def parse(self, response):
        pass
