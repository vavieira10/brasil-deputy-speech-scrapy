import scrapy
from camara_speeches import parser
from camara_speeches import static
import asyncio

class CamaraSiteSpeechesSpider(scrapy.Spider):
    name = 'camara_site_speeches'
    custom_settings = {
        "FEED_URI": "./outputs/discursos_camara.pickle"
    }

    def start_requests(self):
        self.logger.info("[camara_site_speeches] START CRAWLING")
        if self.year == "":
            self.year = "1985"
    
        self._input = parser.get_site_date_inputs(int(self.year))

        base_url = f"{static.SPEECHES_SITE_BASE_URL}{static.SPEECHES_SITE_COMPLEMENT_URL}"
        yield scrapy.Request(
            url=parser.generate_search_url_with_query_object(
                base_url,
                static.get_site_base_query(
                    init_date=self._input["init_date"],
                    end_date=self._input["end_date"]
                )
            ),
            callback=self._first_camara_speeches_request
        )
    
    def _first_camara_speeches_request(self, response):
        self.logger.info("_first_camara_speeches_request")

        amount_of_pages = parser.get_site_amount_of_pages(response)
        if amount_of_pages is None:
            self.logger.error("Amount of pages were not parsed correctly")
            raise RuntimeError("Amount of pages were not parsed correctly")
        
        base_url = f"{static.SPEECHES_SITE_BASE_URL}{static.SPEECHES_SITE_COMPLEMENT_URL}"

        for page in range(1, amount_of_pages+1):
            yield scrapy.Request(
                url=parser.generate_search_url_with_query_object(
                    base_url,
                    static.get_site_base_query(
                        init_date=self._input["init_date"],
                        end_date=self._input["end_date"],
                        page=str(page)
                    )
                ),
                callback=self._camara_speeches_page
            )
    
    def _camara_speeches_page(self, response):
        self.logger.info("_camara_speeches_page")

        speeches = parser.parse_speeches_metadata_from_result_page(response)
        for speech in speeches:
            speech_url = speech.get("discurso", {}).get("url")
            if speech_url is None:
                yield speech
                continue
            
            url = f"{static.SPEECHES_SITE_BASE_URL}{speech_url}"
            yield scrapy.Request(
                url=url,
                cb_kwargs={
                    "speech": speech
                },
                callback=self._speech_transcription_page
            )
    
    def _speech_transcription_page(self, response, speech):
        self.logger.info("_speech_pages")

        transcription = parser.parse_speech_transcription(response)
        speech["discurso"]["transcricao"] = transcription

        yield speech
    


