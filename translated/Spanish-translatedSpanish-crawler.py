import requests
import networkx as nx
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad requests
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for link in soup.find_all('a', href=True):
        absolute_url = urljoin(url, link['href'])
        links.append(absolute_url)
    return links

seed_link = "http://www.facebook.com"
crawled_links = set(get_all_links(seed_link))

master_links = {}
count = 1
for link in tqdm(crawled_links, desc="Processing"):
    temp = list(set(get_all_links(link)))
    master_links[link] = temp

with open('master_links.json', 'w') as json_file:
    json.dump(master_links, json_file, indent=2)

print(master_links)