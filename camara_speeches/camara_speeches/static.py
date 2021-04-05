DEPUTIES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados"
SPEECHES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados/:id/discursos"

BASE_DEPUTIES_QUERY = {
    "ordem": "ASC",
    "ordenaPor": "idLegislatura",
    "itens": "1000",
    "dataInicio": "1989-01-01",
    "dataFim": "2021-04-05"
}