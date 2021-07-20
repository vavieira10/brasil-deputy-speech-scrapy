import scrapy
from camara_speeches import parser
from camara_speeches import static
import asyncio

class CamaraDeputiesSpider(scrapy.Spider):
    name = 'camara_deputies'

    custom_settings = {
        "FEED_URI": "./camara_deputies.json",
        "FEED_FORMAT": 'json',
        "FEED_EXPORT_ENCODING": 'utf-8',
        "FEED_OVERWRITE": True
    }

    def start_requests(self):
        self.logger.info("[camara_deputies] START CRAWLING")
        self._deputies = {}
        self._pages_queue = asyncio.Queue()

        yield scrapy.Request(
            url=parser.generate_search_url_with_query_object(
                static.DEPUTIES_BASE_URL,
                static.get_base_query()
            ),
            callback=self._first_deputies_request
        )
    
    def _first_deputies_request(self, response):
        self.logger.info("_first_deputies_request")
        amount_pages = parser.get_amount_pages(response.body)

        if amount_pages is None:
            raise scrapy.exceptions.CloseSpider("[_first_deputies_request] Error when parsing number of pages")
        
        page_deputies = parser.get_data_from_json(response.body)
        if page_deputies == []:
            raise scrapy.exceptions.CloseSpider("No deputies found")
        
        parser.parse_page_deputies(page_deputies, self._deputies)

        for page in range(2, amount_pages+1):
            self.logger.info(f"[_first_deputies_request] PAGE = {page}")
            self._pages_queue.put_nowait(1)
            yield scrapy.Request(
                url=parser.generate_search_url_with_query_object(
                    static.DEPUTIES_BASE_URL,
                    static.get_base_query(),
                    page=page
                ),
                callback=self._on_deputies_page
            )
    
    def _on_deputies_page(self, response):
        self.logger.info("_on_deputies_page")
        
        page_deputies = parser.get_data_from_json(response.body)
        if page_deputies == []:
            raise scrapy.exceptions.CloseSpider("No deputies found")
        
        parser.parse_page_deputies(page_deputies, self._deputies)
        
        self._pages_queue.get_nowait()
        if self._pages_queue.empty():
            return self._deputies