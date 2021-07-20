# brasil-deputy-speech-scrapy
Scraper for crawling Brasil Camara dos Deputados (Chamber of Deputies) speeches.


For more information https://dadosabertos.camara.leg.br/swagger/api.html#api

This scraper crawls for deputies speeches from `1985-03-15` to `2021-04-05` by default

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

The scraper was splitted in two steps:

1. Fetching all deputies from start date to end date;
2. Given the deputies and its legislatures, capture the speeches.

## Run the following command for **crawling only the deputies data**

```
make crawl-deputies
```

The deputies data will be saved as a `json` file named `./camara_deputies.json`

## Run the following command for **crawling only the speeches data, but it requires the deputies data first**

```
make crawl-speeches
```

## Run the following command for **crawling only the speeches data from the website**
**This variation was implemented because the Camara API hasn't all the speeches when consulting it.**
The data was scraped from the site https://www2.camara.leg.br/atividade-legislativa/discursos-e-notas-taquigraficas

The arg `year` is not required, but if is not passed, the default year is **1985**

If the year 1985 is passed, the date range will be from 1985-03-15 to 1985-12-31, because 03-15 of that year was the first
day of the Jose Sarney presidency mandat.

**From 1985 to mid 2000, there are no transcripted speeches, only the PDF or IMAGE files with the speech.**

### **When scraping each year indepedently, it will append every speech of a year to the ./outputs/discursos_camara.pickle file**

```
make crawl-site-speeches year=2003
``` 

### For scraping speeches for a date range, you can use the `crawl_speeches_from_date_ranges.sh` script.

```
./crawl_speeches_from_date_ranges.sh START_YEAR END_YEAR
```

For crawling data from 1985 to 2021, for example, simply run the following command:
```
./crawl_speeches_from_date_ranges.sh 1985 2021
```

## Run the following command for **running both steps**

The speeches will be saved as a `pickle` file named `./outputs/camara_speeches.pickle`

```
make crawl-all
```

Since the deputies data were already captured, you may simply run the `make crawl-speeches` directly

# Output example from API crawled speeches
```json
{
  "dataHoraInicio": "2001-03-21T15:10",
  "dataHoraFim": null,
  "uriEvento": "",
  "faseEvento": {
    "titulo": "Pequeno Expediente",
    "dataHoraInicio": null,
    "dataHoraFim": null
  },
  "tipoDiscurso": "PEQUENO EXPEDIENTE",
  "urlTexto": "http://imagem.camara.leg.br/dc_20b.asp?largura=&altura=&tipoForm=diarios&selCodColecaoCsv=D&Datain=22%2F3%2F2001&txPagina=6429&txSuplemento=&enviar=Pesquisar",
  "urlAudio": null,
  "urlVideo": null,
  "keywords": "ABUSO, PROGRAMAÇÃO, TELEVISÃO, OFENSA, MORAL, COSTUMES.\r\nCONSTITUIÇÃO FEDERAL, CONSELHO DE COMUNICAÇÃO SOCIAL.",
  "sumario": "Urgente tramitação da proposta de emenda constitucional sobre as atribuições do Conselho Consultivo do Conselho de Comunicação Social.",
  "transcricao": "O SR. AROLDE DE OLIVEIRA (Bloco/PFL-RJ. Sem revisão do orador. ) - Sr. Presidente, Sras. e Srs. Deputados, venho a esta tribuna fazer rápida análise sobre o uso dos meios de comunicação no Brasil. Vez por outra, Deputados e Deputadas levantam a questão do abuso e da ofensa à moral e aos bons costumes em programas veiculados nos meios de comunicação de massa.\r\n\tNa verdade, a Constituição brasileira, nos arts. 220 a 224, deu um avanço muito grande, quando reuniu neste Capítulo todo o aspecto de defesa dos direitos intelectuais, das liberdades de expressão e, ao mesmo tempo, estabeleceu as regras administrativas, regras básicas dos mecanismos de concessão para esses meios de comunicação de massa, em particular o rádio e a televisão.\r\n\tNa mesma época e no mesmo Capítulo, a Constituição previu a criação do Conselho de Comunicação Social, com atribuições amplas sobre toda a matéria incluída naquele capítulo. O conselho foi instituído em 1991, pela Lei n.º 8.389, e, desde então, vem aguardando sua instalação que também tem sido objeto de reclamação e de discussão nesta Casa. \r\n\tO Conselho tornou-se um pólo de antagonismo, com as reformas que aconteceram na Constituição, principalmente aquelas no setor de telecomunicações, que, com a Lei Geral de Telecomunicações, trouxeram outros órgãos com as mesmas atribuições que deveriam ser desse conselho. \r\n\tUma lei específica que regulamentava a TV por assinatura através de cabo por linha física estabeleceu que o Conselho deveria opinar, inclusive, nas autorizações para aqueles serviços. Criou-se então um impasse e esse conselho não pôde, desde então, ser instalado. \r\n\tPropus, em emenda constitucional que está tramitando na Casa, que fizéssemos no Capítulo da Comunicação Social da Constituição uma separação dos assuntos que tratam do conteúdo da mensagem daqueles que tratam da administração, da gerência, enfim, da concessão dos veículos. E que atribuíssemos ao Conselho Consultivo, do Conselho Nacional de Comunicação Social, apenas as atribuições de análises do conteúdo. Deste modo, teríamos, como órgão consultivo da Câmara dos Deputados e do Congresso Nacional, um conselho representado por toda a sociedade, que poderia opinar e estabelecer limites para as mensagens ou para o conteúdo das mensagens veiculadas nos meios de comunicação de massa, em particular os meios abertos, ou seja, rádio e televisão.\r\n\tSr. Presidente, essa emenda está em tramitação, e vou agir junto a minha Liderança do PFL para que possamos agilizá-la. Assim, teremos condição de instalar, de vez, o Conselho de Comunicação Social. De outra forma, não vejo jeito, porque esse conselho, como está hoje, com as atribuições a ele atribuídas — desculpem-me a redundância — não pode ser instalado porque vai bater de frente, vai ter problemas com a ANATEL, com o próprio Ministério das Comunicações, nas suas atribuições mais recentes.\r\nSr. Presidente, Sras. e Srs. Deputados, era este o registro que eu queria fazer.",
  "nomeDeputado": "AROLDE DE OLIVEIRA",
  "partidosDeputado": [
    { "siglaPartido": "PFL", "idLegislatura": "47" },
    { "siglaPartido": "PFL", "idLegislatura": "48" },
    { "siglaPartido": "PFL", "idLegislatura": "49" },
    { "siglaPartido": "PFL", "idLegislatura": "50" },
    { "siglaPartido": "PSD", "idLegislatura": "55" },
    { "siglaPartido": "DEM", "idLegislatura": "53" },
    { "siglaPartido": "PSD", "idLegislatura": "54" },
    { "siglaPartido": "PFL", "idLegislatura": "52" },
    { "siglaPartido": "PFL", "idLegislatura": "51" }
  ],
  "ufsDeputado": ["RJ"]
}
```

# Output example from website crawled speeches
```json
{
  "dataDiscurso": "01/07/2003",
  "tituloSessao": "001.1.52.E",
  "fase": "PROPOSIÇÕES",
  "deputado": { "nome": "ALEX CANZIANI", "siglaPartido": "PTB", "uf": "PR" },
  "horaDiscurso": "20h14",
  "publicacao": {
    "url": null,
    "titulo": "DCD02/07/2003 PAG. 30329"
  },
  "sumario": "\r\n\t\t\t\t\tTranscurso do 7º aniversário de fundação da TV Tarubá, no Município de Londrina, Estado do Paraná. Anúncio de reunião do Ministro das Comunicações, Miro Teixeira, com representantes do PROCON para definição de ações contra o aumento de tarifas telefônicas autorizado pela ANATEL.\r\n\t\t\t\t",
  "discurso": {
    "url": "TextoHTML.asp?etapa=5\r\n\t\t\t\t\t\t\t&nuSessao=001.1.52.E\r\n\t\t\t\t\t\t\t&nuQuarto=188\r\n\t\t\t\t\t\t\t&nuOrador=3\r\n\t\t\t\t\t\t\t&nuInsercao=0\r\n\t\t\t\t\t\t\t&dtHorarioQuarto=20:14\r\n\t\t\t\t\t\t\t&sgFaseSessao=PR\r\n\t\t\t\t\t\t\t&Data=01/07/2003\r\n\t\t\t\t\t\t\t&txApelido=ALEX CANZIANI, PTB-PR\r\n\t\t\t\t\t\t\t&txFaseSessao=Proposições\r\n\t\t\t\t\t\t\t&txTipoSessao=Ordinária - CD\r\n\t\t\t\t\t\t\t&dtHoraQuarto=20:14\r\n\t\t\t\t\t\t\t&txEtapa=",
    "transcricao": "O SR. ALEX CANZIANI (PTB-PR. Pela ordem. Sem revisão do orador.) - Sr. Presidente, abordarei rapidamente 2 assuntos. Primeiro cumprimento a TV Tarubá, do Município de Londrina, pelo transcurso dos seus 7 anos de existência. Cumprimento todos os diretores pelo belo trabalho que desenvolvem em prol não só de Londrina, mas de todo o norte do Paraná.Quero também dizer, Sr. Presidente, que, junto com os Deputados Givaldo Carimbão e Luiz Bittencourt, fomos ao Ministério das Comunicações para falar com o Ministro Miro Teixeira a respeito desses aumentos abusivos de tarifas telefônicas a que a população brasileira está sendo submetida.Não é possível que tenhamos aumentos dessa envergadura, fazendo com que o cidadão se sinta impotente em face do que fez a ANATEL. Vamos fazer na próxima quinta-feira, com a presença do Sr. Ministro e de representantes de todos os PROCONs do País, reunião para definir como ingressaremos com ações contra esse abuso. Em meu Município, Londrina, administrada pelo Partido dos Trabalhadores, temos uma companhia municipal, a SERCONTEL, e não entendemos por que esse mesmo aumento abusivo está sendo por ela adotado para atender à cidade. Ora, essa companhia, que é superavitária, teria todas as condições de não repassar esse aumento abusivo, até porque a espelho, a GVT, não está cobrando nenhum aumento de seus consumidores. Deixo aqui o apelo para revertermos isso. Essa reunião que faremos será de grande importância, para que a sociedade brasileira veja a participação da Câmara dos Deputados.Muito obrigado."
  }
}
```