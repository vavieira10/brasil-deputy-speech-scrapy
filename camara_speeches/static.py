DEPUTIES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados"
SPEECHES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/discursos"


def get_base_query(
        init_date="1985-03-15",
        end_date="2021-04-07",
        order_by="idLegislatura",
        itens="1000"
    ):
    return  {
        "ordem": "ASC",
        "ordenarPor": order_by,
        "itens": itens,
        "dataInicio": init_date,
        "dataFim": end_date
    }