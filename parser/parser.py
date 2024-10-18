import time
import json
import random
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://dnd.su'
BESTIARY_URL = 'https://dnd.su/articles/bestiary/'
RULES_URL = 'https://dnd.su/articles/mechanics/536-how-to-start-playing-dd/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'}


def get_bestiary() -> None:
    response = requests.get(BESTIARY_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", {"class": "read-more"})
    bestiary = {}
    for link in links:
        time.sleep(random.random() * 10)
        response = requests.get(BASE_URL + link['href'], headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("h2", {"class": "card-title"}).findNext('a').text
        descriptions = soup.find('div', {'class': 'desc card__article-body'}).findAllNext('p')
        description = ''
        for desc in descriptions:
            description += desc.text
        bestiary[title] = description

    print(bestiary)

    with open('data/bestiary.json', 'w') as file:
        json.dump(bestiary, file, indent=4, ensure_ascii=False)

    with open('data/bestiary.md', 'w') as file:
        for title, description in bestiary.items():
            file.write(f"## {title}\n{description}\n")

    return


def get_rules() -> None:
    response = requests.get(RULES_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    rules = ''
    for p in soup.find('div', {'class': 'desc card__article-body'}).findAll('p'):
        rules += p.text
    with open('data/rules.md', 'w') as f:
        f.write(rules)
    return
