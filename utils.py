import requests
from bs4 import BeautifulSoup

def get_soup(url):
    response = requests.get(url, headers={"User-Agent": "gbc"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup
