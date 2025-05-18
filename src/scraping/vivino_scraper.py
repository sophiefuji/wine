import json
import time
import random
import requests
from bs4 import BeautifulSoup

def scrape_vivino_wine(wine_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                      " (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(wine_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {wine_url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # This is pseudocode: structure changes often on Vivino, this will need to be adapted
    wine_id = wine_url.split("/")[-1]
    name = soup.find("h1").text.strip()
    vintage = soup.find("div", class_="vintage").text.strip()
    region = soup.find("div", class_="region").text.strip()
    grapes = [g.text.strip() for g in soup.select(".grape")]
    producer = soup.find("div", class_="producer").text.strip()

    wine_data = {
        "wine_id": wine_id,
        "name": name,
        "vintage": vintage,
        "region": region,
        "grapes": grapes,
        "producer": producer
    }

    return wine_data

def scrape_multiple_wines(url_list, output_file="data/raw/vivino_wines.json"):
    all_wines = []
    for url in url_list:
        try:
            wine_data = scrape_vivino_wine(url)
            all_wines.append(wine_data)
            print(f"Scraped: {wine_data['name']}")
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    with open(output_file, "w") as f:
        json.dump(all_wines, f, indent=2)

    print(f"Saved {len(all_wines)} records to {output_file}")
