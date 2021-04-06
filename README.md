# brasil-deputy-speech-scrapy
Scraper for crawling Brasil Camara dos Deputados (Chamber of Deputies) speeches.


For more information https://dadosabertos.camara.leg.br/swagger/api.html#api

This scraper crawls for deputies speeches from `1989-01-01` to `2021-04-05` by default

# Requirements

- Python3
- virtualenv

# Setting up Python virtual enviroment

## Steps for creating and activating the virtualenv (Ubuntu/MacOS)

1. ```python3 -m venv scraper_virtualenv```
2. ```source scraper_virtualenv/bin/activate```
3. ```pip install --upgrade pip```

## Steps for installing the dependencies
Run the following command once inside the virtualenv

1. ```pip install -r requirements.txt```

##  Steps for leaving the virtualenv
Simply run the following command

1. ```deactivate```

# Running the scraper

Run the following command

```
make crawl-speeches
```