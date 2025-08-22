import requests
import time
import re

def get_pgns(get_archives_url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
    }
    response = requests.get(get_archives_url, headers=headers)
    time.sleep(10)
    response.raise_for_status()
    archives_data = response.json()

    archives_urls = archives_data["archives"]

    all_pgns = []

    for i, archives_url in enumerate(archives_urls):
        time.sleep(1)
        pgn_url = f"{archives_url}/pgn"
        pgn_response = requests.get(pgn_url, headers=headers)
        pgn_response.raise_for_status()
        pgn = re.split(r"{.*?}", pgn_response.text)
        pgns = []
        for pgn_element in pgn:
            pgn_element.split("\n\n\n")
            pgns.append(pgn_element)
        all_pgns.append(pgns)
        all_pgns_formatted=""
        for element in all_pgns:
            if isinstance(element, list):
                for final_element in element:
                    all_pgns_formatted+=final_element
            else:
                all_pgns_formatted+=element

    return all_pgns_formatted

def pgn(archive_url):
    return get_pgns(archive_url)

"""print(pgn("https://api.chess.com/pub/player/ezypoliorz27/games/archives"))"""