#!/usr/bin/env python3

from scrapers import PoolScraper

webs = {
    'Sutka': {'url': 'http://www.sutka.eu', 'reg': r'Aktuální počet návštěvníků: (?P<people>[\d]*)'}
}

for k, v in webs.items():
    a = PoolScraper(v['url'], v['reg'])
    print(a.read())
