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
  "keywords": "ABUSO, PROGRAMA????O, TELEVIS??O, OFENSA, MORAL, COSTUMES.\r\nCONSTITUI????O FEDERAL, CONSELHO DE COMUNICA????O SOCIAL.",
  "sumario": "Urgente tramita????o da proposta de emenda constitucional sobre as atribui????es do Conselho Consultivo do Conselho de Comunica????o Social.",
  "transcricao": "O SR. AROLDE DE OLIVEIRA (Bloco/PFL-RJ. Sem revis??o do orador. ) - Sr. Presidente, Sras. e Srs. Deputados, venho a esta tribuna fazer r??pida an??lise sobre o uso dos meios de comunica????o no Brasil. Vez por outra, Deputados e Deputadas levantam a quest??o do abuso e da ofensa ?? moral e aos bons costumes em programas veiculados nos meios de comunica????o de massa.\r\n\tNa verdade, a Constitui????o brasileira, nos arts. 220 a 224, deu um avan??o muito grande, quando reuniu neste Cap??tulo todo o aspecto de defesa dos direitos intelectuais, das liberdades de express??o e, ao mesmo tempo, estabeleceu as regras administrativas, regras b??sicas dos mecanismos de concess??o para esses meios de comunica????o de massa, em particular o r??dio e a televis??o.\r\n\tNa mesma ??poca e no mesmo Cap??tulo, a Constitui????o previu a cria????o do Conselho de Comunica????o Social, com atribui????es amplas sobre toda a mat??ria inclu??da naquele cap??tulo. O conselho foi institu??do em 1991, pela Lei n.?? 8.389, e, desde ent??o, vem aguardando sua instala????o que tamb??m tem sido objeto de reclama????o e de discuss??o nesta Casa. \r\n\tO Conselho tornou-se um p??lo de antagonismo, com as reformas que aconteceram na Constitui????o, principalmente aquelas no setor de telecomunica????es, que, com a Lei Geral de Telecomunica????es, trouxeram outros ??rg??os com as mesmas atribui????es que deveriam ser desse conselho. \r\n\tUma lei espec??fica que regulamentava a TV por assinatura atrav??s de cabo por linha f??sica estabeleceu que o Conselho deveria opinar, inclusive, nas autoriza????es para aqueles servi??os. Criou-se ent??o um impasse e esse conselho n??o p??de, desde ent??o, ser instalado. \r\n\tPropus, em emenda constitucional que est?? tramitando na Casa, que fiz??ssemos no Cap??tulo da Comunica????o Social da Constitui????o uma separa????o dos assuntos que tratam do conte??do da mensagem daqueles que tratam da administra????o, da ger??ncia, enfim, da concess??o dos ve??culos. E que atribu??ssemos ao Conselho Consultivo, do Conselho Nacional de Comunica????o Social, apenas as atribui????es de an??lises do conte??do. Deste modo, ter??amos, como ??rg??o consultivo da C??mara dos Deputados e do Congresso Nacional, um conselho representado por toda a sociedade, que poderia opinar e estabelecer limites para as mensagens ou para o conte??do das mensagens veiculadas nos meios de comunica????o de massa, em particular os meios abertos, ou seja, r??dio e televis??o.\r\n\tSr. Presidente, essa emenda est?? em tramita????o, e vou agir junto a minha Lideran??a do PFL para que possamos agiliz??-la. Assim, teremos condi????o de instalar, de vez, o Conselho de Comunica????o Social. De outra forma, n??o vejo jeito, porque esse conselho, como est?? hoje, com as atribui????es a ele atribu??das ??? desculpem-me a redund??ncia ??? n??o pode ser instalado porque vai bater de frente, vai ter problemas com a ANATEL, com o pr??prio Minist??rio das Comunica????es, nas suas atribui????es mais recentes.\r\nSr. Presidente, Sras. e Srs. Deputados, era este o registro que eu queria fazer.",
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
  "fase": "PROPOSI????ES",
  "deputado": { "nome": "ALEX CANZIANI", "siglaPartido": "PTB", "uf": "PR" },
  "horaDiscurso": "20h14",
  "publicacao": {
    "url": null,
    "titulo": "DCD02/07/2003 PAG. 30329"
  },
  "sumario": "\r\n\t\t\t\t\tTranscurso do 7?? anivers??rio de funda????o da TV Tarub??, no Munic??pio de Londrina, Estado do Paran??. An??ncio de reuni??o do Ministro das Comunica????es, Miro Teixeira, com representantes do PROCON para defini????o de a????es contra o aumento de tarifas telef??nicas autorizado pela ANATEL.\r\n\t\t\t\t",
  "discurso": {
    "url": "TextoHTML.asp?etapa=5\r\n\t\t\t\t\t\t\t&nuSessao=001.1.52.E\r\n\t\t\t\t\t\t\t&nuQuarto=188\r\n\t\t\t\t\t\t\t&nuOrador=3\r\n\t\t\t\t\t\t\t&nuInsercao=0\r\n\t\t\t\t\t\t\t&dtHorarioQuarto=20:14\r\n\t\t\t\t\t\t\t&sgFaseSessao=PR\r\n\t\t\t\t\t\t\t&Data=01/07/2003\r\n\t\t\t\t\t\t\t&txApelido=ALEX CANZIANI, PTB-PR\r\n\t\t\t\t\t\t\t&txFaseSessao=Proposi????es\r\n\t\t\t\t\t\t\t&txTipoSessao=Ordin??ria - CD\r\n\t\t\t\t\t\t\t&dtHoraQuarto=20:14\r\n\t\t\t\t\t\t\t&txEtapa=",
    "transcricao": "O SR. ALEX CANZIANI (PTB-PR. Pela ordem. Sem revis??o do orador.) - Sr. Presidente, abordarei rapidamente 2 assuntos. Primeiro cumprimento a TV Tarub??, do Munic??pio de Londrina, pelo transcurso dos seus 7 anos de exist??ncia. Cumprimento todos os diretores pelo belo trabalho que desenvolvem em prol n??o s?? de Londrina, mas de todo o norte do Paran??.Quero tamb??m dizer, Sr. Presidente, que, junto com os Deputados Givaldo Carimb??o e Luiz Bittencourt, fomos ao Minist??rio das Comunica????es para falar com o Ministro Miro Teixeira a respeito desses aumentos abusivos de tarifas telef??nicas a que a popula????o brasileira est?? sendo submetida.N??o ?? poss??vel que tenhamos aumentos dessa envergadura, fazendo com que o cidad??o se sinta impotente em face do que fez a ANATEL. Vamos fazer na pr??xima quinta-feira, com a presen??a do Sr. Ministro e de representantes de todos os PROCONs do Pa??s, reuni??o para definir como ingressaremos com a????es contra esse abuso. Em meu Munic??pio, Londrina, administrada pelo Partido dos Trabalhadores, temos uma companhia municipal, a SERCONTEL, e n??o entendemos por que esse mesmo aumento abusivo est?? sendo por ela adotado para atender ?? cidade. Ora, essa companhia, que ?? superavit??ria, teria todas as condi????es de n??o repassar esse aumento abusivo, at?? porque a espelho, a GVT, n??o est?? cobrando nenhum aumento de seus consumidores. Deixo aqui o apelo para revertermos isso. Essa reuni??o que faremos ser?? de grande import??ncia, para que a sociedade brasileira veja a participa????o da C??mara dos Deputados.Muito obrigado."
  }
}
```