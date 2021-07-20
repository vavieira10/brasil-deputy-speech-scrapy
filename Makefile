
clear-deputies:
	rm -f ./camara_deputies.json

clear-speeches:
	rm -f ./outputs/camara_speeches.pickle

crawl-deputies: clear-deputies
	scrapy crawl camara_deputies

crawl-speeches: clear-speeches
	scrapy crawl camara_speeches

crawl-site-speeches:
	scrapy crawl camara_site_speeches -a year=$(year)

crawl-all: crawl-deputies crawl-speeches

