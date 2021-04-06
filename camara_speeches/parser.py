import json
import re
from urllib.parse import urlencode

_get_page_re = re.compile(r"pagina\s*=\s*(\d+)")

def json_to_dict(body):
    try:
        return json.loads(body)
    except:
        return None


def generate_search_url_with_query(base_url, queries_object, page=1):
    queries_object.update({
        "pagina": str(page)
    })
    query_string = urlencode(queries_object)

    return f"{base_url}?{query_string}"


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