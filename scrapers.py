import requests
import re


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
        data = self.parse(text, self.reg)
        return data
