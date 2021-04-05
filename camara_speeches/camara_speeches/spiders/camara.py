import scrapy
from camara_speeches import parser
from camara_speeches import static
import asyncio

class CamaraSpider(scrapy.Spider):
    name = 'camara'
    def start_request(self):
        yield scrapy.Request(
            url=parser.generate_search_url_with_query(
                static.BASE_DEPUTIES_QUERY,
                static.BASE_DEPUTIES_QUERY
            ),
            callback=self.first_request
        )

    def first_request(self, response):
        pass
