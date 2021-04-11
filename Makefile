
clear-deputies:
	rm -f ./camara_deputies.json

clear-outputs:
	rm -f ./outputs/*

crawl-deputies: clear-deputies
	scrapy crawl camara_deputies

crawl-speeches: clear-outputs
	scrapy crawl camara_speeches

crawl-all: crawl-deputies crawl-speeches

