#!/usr/bin/env python3

import re
import requests


class PoolScraper(object):
    def __init__(self, url, reg):

        self.url = url
        self.reg = reg

    def download(self, url):
        return requests.get(url).text

    def scrape(self, html):
        return html

    def parse(self, text, reg):
        match = re.search(reg, text)
        if match:
            return match.groupdict()
        else:
            return None

    def read(self):
        html = self.download(self.url)
        text = self.scrape(html)
        print(text)
        print(self.reg)
        data = self.parse(text, self.reg)
        return data


webs = {
    'Sutka': {'url': 'http://www.sutka.eu', 'reg': r'Aktuální počet návštěvníků: (?P<people>[\d]*)'}
    }

for k, v in webs.items():
    a = PoolScraper(v['url'], v['reg'])
    print(a.read())
