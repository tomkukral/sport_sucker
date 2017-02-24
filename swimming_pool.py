#!/usr/bin/env python3

from bs4 import BeautifulSoup
from requests import get

html_doc = get('http://www.sutka.eu/').text

soup = BeautifulSoup(html_doc, 'html.parser')

t = soup.find(id='header-content').p.text.strip()

print(t)
