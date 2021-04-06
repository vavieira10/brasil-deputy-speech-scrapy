import scrapy
from camara_speeches import parser
from camara_speeches import static
import asyncio

class CamaraSpeechesSpider(scrapy.Spider):
    name = 'camara_speeches'

    def start_requests(self):
        self.logger.info("START CRAWLING")
        yield scrapy.Request(
            url=parser.generate_search_url_with_query(
                static.DEPUTIES_BASE_URL,
                static.get_base_query(init_date="2018-01-01")
            ),
            callback=self._first_request
        )

    def _first_request(self, response):
        self.logger.info("_first_request")
        amount_pages = parser.get_amount_pages(response.body)

        if amount_pages is None:
            raise scrapy.exceptions.CloseSpider("[_first_request] Error when parsing number of pages")

        for page in range(1, amount_pages+1):
            self.logger.info(f"[_first_request] PAGE = {page}")
            yield scrapy.Request(
                url=parser.generate_search_url_with_query(
                    static.DEPUTIES_BASE_URL,
                    static.get_base_query(init_date="2018-01-01"),
                    page=page
                ),
                callback=self._on_deputies_page
            )
    
    def _on_deputies_page(self, response):
        self.logger.info("_on_deputies_page")
        data = parser.json_to_dict(response.body)

        deputies = data.get("dados", [])
        if deputies == []:
            raise scrapy.exceptions.CloseSpider("No deputies found")
        
        for dep in deputies:
            base_url = static.SPEECHES_BASE_URL.format(id=dep.get("id", ""))
            query = static.get_base_query(order_by="dataHoraInicio", itens="100")
            query.update({
                "idLegislatura": dep.get("idLegislatura")
            })
            yield scrapy.Request(
                url=parser.generate_search_url_with_query(
                    base_url,
                    query,
                ),
                cb_kwargs={
                    "deputies_base_url": base_url,
                    "query": query
                },
                callback=self._on_speeches_page
            )

    def _on_speeches_page(self, response, deputies_base_url, query):
        self.logger.info("_on_speeches_page")
        amount_pages = parser.get_amount_pages(response.body)

        if amount_pages is not None:
            for page in range(1, amount_pages+1):
                yield scrapy.Request(
                    url=parser.generate_search_url_with_query(
                        deputies_base_url,
                        query,
                        page=page
                    ),
                    callback=self._dispatch_speeches
                )
    

    def _dispatch_speeches(self, response):
        self.logger.info("_dispatch_speeches")
        data = parser.json_to_dict(response.body)
        speeches = data.get("dados", [])

        for sp in speeches:
            yield sp