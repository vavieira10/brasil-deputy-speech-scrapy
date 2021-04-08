import json
import re
from urllib.parse import urlencode

_get_page_re = re.compile(r"pagina\s*=\s*(\d+)")

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


def get_page_from_url(url):
    try:
        page_search = _get_page_re.search(url)
        return convert_to_int(page_search.group(1))
    except:
        return None