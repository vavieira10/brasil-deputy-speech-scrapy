import scrapy
from camara_speeches import parser
from camara_speeches import static
import json

class CamaraSpeechesSpider(scrapy.Spider):
    name = 'camara_speeches'

    def start_requests(self):
        self.logger.info("[camara_speeches] START CRAWLING")

        deputies = []
        try:
            with open("./camara_deputies.json", "r") as f:
                deputies = json.load(f)
        except:
            pass
        
        if deputies == []:
            raise scrapy.exceptions.CloseSpider("[camara_speeches] Error when loading deputies file")
        
        self._deputies = deputies[0]
        self._num_deputies = len(self._deputies.keys())
        self.logger.info(f"START: NUMBER OF DEPUTIES = {self._num_deputies}")

        for dep_id, dep_data in self._deputies.items():
            leg_ids = dep_data["idLegislaturas"]
            base_url = static.SPEECHES_BASE_URL.format(id=dep_id)
            base_query_object = static.get_base_query(order_by="dataHoraInicio", itens="100")
            url = parser.generate_search_url_with_query_object(
                base_url,
                base_query_object
            )

            legs_id_query = parser.generate_leg_ids_query(leg_ids)
            url += legs_id_query
            
            yield scrapy.Request(
                url=url,
                meta={
                    "dep_id": dep_id,
                    "dep_data": dep_data
                },
                cb_kwargs={
                    "deputies_base_url": base_url,
                    "base_query_object": base_query_object,
                    "legs_id_query": legs_id_query
                },
                callback=self._on_speeches_page
            )

    def _on_speeches_page(self, response, deputies_base_url, base_query_object, legs_id_query):
        self._num_deputies -= 1
        self.logger.info(f"[_on_speeches_page], DEP_ID = {response.meta['dep_id']}, NUM_DEPUTIES_LEFT = {self._num_deputies}")
        amount_pages = parser.get_amount_pages(response.body)

        if amount_pages is not None:
            speeches = parser.get_data_from_json(response.body)
            for sp in speeches:
                sp.update({
                    "nomeDeputado": response.meta["dep_data"]["nome"],
                    "partidosDeputado": response.meta["dep_data"]["partidos"],
                    "ufsDeputado": response.meta["dep_data"]["ufs"]
                })
                yield sp

            if amount_pages > 1:
                for page in range(2, amount_pages+1):
                    self.logger.info(f"[_on_speeches_page] PAGE = {page}")
                    
                    url = parser.generate_search_url_with_query_object(
                        deputies_base_url,
                        base_query_object,
                        page=page
                    )

                    url += legs_id_query

                    yield scrapy.Request(
                        url=url,
                        meta={
                            "dep_data": response.meta["dep_data"]
                        },
                        callback=self._dispatch_speeches
                    )
    

    def _dispatch_speeches(self, response):
        self.logger.info("_dispatch_speeches")
        speeches = parser.get_data_from_json(response.body)

        for sp in speeches:
            sp.update({
                "nomeDeputado": response.meta["dep_data"]["nome"],
                "partidosDeputado": response.meta["dep_data"]["partidos"],
                "ufsDeputado": response.meta["dep_data"]["ufs"]
            })
            yield sp