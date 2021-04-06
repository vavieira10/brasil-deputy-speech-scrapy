
clear-outputs:
	rm -f ./outputs/*

crawl-speeches: clear-outputs
	scrapy crawl camara_speeches

