DEPUTIES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados"
SPEECHES_BASE_URL = "https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/discursos"
SPEECHES_SITE_BASE_URL = "https://www.camara.leg.br/internet/sitaqweb/"
SPEECHES_SITE_COMPLEMENT_URL = "resultadoPesquisaDiscursos.asp?"

def get_site_base_query(init_date="15/03/1985", end_date="31/12/1985", page_size="50", page="1"):
    return {
        "txIndexacao": "",
        "CurrentPage": page,
        "txOrador": "",
        "txPartido": "",
        "txUF": "",
        "dtInicio": init_date,
        "dtFim": end_date,
        "txTexto": "",
        "txSumario": "",
        "basePesq": "plenario",
        "cammpoOrdenacao": "dtSessao",
        "PageSize": page_size,
        "TipoOrdenacao": "ASC",
        "btnPesq": "Pesquisar"
    }


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
