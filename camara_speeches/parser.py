import json
import re
from html import unescape
from urllib.parse import urlencode

_get_page_re = re.compile(r"pagina\s*=\s*(\d+)")
_get_site_page_re = re.compile(r"CurrentPage=(\d+)")

def json_to_dict(body):
    try:
        return json.loads(body)
    except:
        return None


def get_data_from_json(body):
    data = json_to_dict(body)
    return data.get("dados", [])


def parse_page_deputies(page_deputies, output_data):
    for dep in page_deputies:
        dep_id = str(dep["id"])
        dep_id_leg = str(dep["idLegislatura"])
        party = dep["siglaPartido"]
        uf = dep["siglaUf"]
        
        if output_data.get(dep_id, {}) == {}:
            output_data[dep_id] = {
                "nome": dep.get("nome", ""),
            }
        

        if output_data.get(dep_id, {}).get("ufs", []) == []:
            output_data[dep_id]["ufs"] = []
        output_data[dep_id]["ufs"].append(uf)
        output_data[dep_id]["ufs"] = list(set(output_data[dep_id]["ufs"]))

        if output_data.get(dep_id, {}).get("partidos", []) == []:
            output_data[dep_id]["partidos"] = []
        output_data[dep_id]["partidos"].append({
            "siglaPartido": party,
            "idLegislatura": dep_id_leg
        })
        
        if output_data.get(dep_id, {}).get("idLegislaturas", []) == []:
            output_data[dep_id]["idLegislaturas"] = []
        output_data[dep_id]["idLegislaturas"].append(dep_id_leg)


def generate_search_url_with_query_object(base_url, queries_object, page=1):
    queries_object.update({
        "pagina": str(page)
    })
    query_string = urlencode(queries_object)

    return f"{base_url}?{query_string}"


def generate_leg_ids_query(leg_ids):
    query = ""
    for leg_id in leg_ids:
        query += f"&idLegislatura={leg_id}"
    
    return query


def convert_to_int(value):
    try:
        return int(value)
    except:
        return None


def get_amount_pages(body):
    try:
        response_dict = json_to_dict(body)
        last_link = next(l.get("href") for l in response_dict.get("links", []) if l.get("rel", "").lower() == "last")
        return get_page_from_url(last_link)
    except:
        pass

    return None

def get_site_amount_of_pages(response):
    href = response.xpath("//div[@class='listingBar']/span/a[contains(., 'Última P')]/@href").get()
    if href is None:
        return None
    
    last_page_search = _get_site_page_re.search(href)
    if last_page_search is None:
        return None
    
    return int(last_page_search.group(1))


def get_page_from_url(url):
    try:
        page_search = _get_page_re.search(url)
        return convert_to_int(page_search.group(1))
    except:
        return None


def parse_deputy(text):
    if text is None:
        return None
    
    name_and_party_uf = text.split(",")
    if len(name_and_party_uf) == 1:
        return {
            "nome": text
        }
    name, party_uf = name_and_party_uf
    
    party_and_uf = party_uf.strip(" \r\t\n").split("-")
    uf = ""
    if len(party_and_uf) > 1:
        party, uf = party_and_uf
    else:
        party = party_and_uf[0]

    return {
        "nome": name.strip(" \r\t\n"),
        "siglaPartido": party.strip(" \r\t\n"),
        "uf": uf.strip(" \r\t\n")
    }


def parse_pub(tr):
    href = tr.xpath("./td[8]/a/@href").get()
    pub_title = tr.xpath("./td[8]/a/text()").get()

    return {
        "url": href if href != "#" else None,
        "titulo": unescape(pub_title).strip(" \r\t\n") if pub_title is not None else None
    }


def get_text_data_from_tr(tr, index):
    text = tr.xpath(f"./td[{index}]/text()").get()
    if text is None:
        return None
    
    return text.strip(" \r\t\n")


def speeches_info_from_tr(tr):
    return {
        "dataDiscurso": get_text_data_from_tr(tr, 1),
        "tituloSessao": get_text_data_from_tr(tr, 2),
        "fase": get_text_data_from_tr(tr, 3),
        "deputado": parse_deputy(get_text_data_from_tr(tr, 6)),
        "horaDiscurso": get_text_data_from_tr(tr, 7),
        "publicacao": parse_pub(tr)
    }

def parse_summary(tr):
    summary_text = tr.xpath("./td/text()").get()
    return {
        "sumario": unescape(summary_text)
    }


def parse_speech_url(tr):
    href = tr.xpath("./td[4]/a/@href").get()
    
    return {
        "discurso": {
            "url": href
        }
    }


def parse_speech_transcription(response):
    transcription_texts = response.xpath("//body/p//text()").getall()
    if transcription_texts == []:
        return None
    
    return unescape("".join(transcription_texts))


def parse_speeches_metadata_from_result_page(response):
    speeches = []
    trs = response.xpath("//table/tbody//tr")

    # the step is 2 because even indexes are the speech metadata
    # and the odd indexes are the speech text summary
    for idx in range(0, len(trs), 2):
        speeches_base_info = {}
        speeches_base_info = speeches_info_from_tr(trs[idx])
        speeches_base_info.update(parse_summary(trs[idx+1]))
        speeches_base_info.update(parse_speech_url(trs[idx]))
        speeches.append(speeches_base_info)
    
    return speeches


def get_site_date_inputs(year):
    return {
        "init_date": f"01/01/{year}" if year != 1985 else f"15/03/{year}",
        "end_date": f"31/12/{year}"
    }
