# -*- coding: utf-8 -*-
import requests
import re


class RegexpScraper(object):
    def __init__(self, **kwargs):

        self.url = kwargs.get('url', None)
        self.reg = kwargs.get('reg', None)
        self.method = kwargs.get('method', 'get')
        self.data = kwargs.get('data', '{}')

    def download(self, url, method, data):
        if method == 'post':
            response = requests.post(url, data=data)
            out = response.text.encode(response.encoding)
        else:
            response = requests.get(url)
            out = response.text.encode(response.encoding)

        print(url)

        return out

    def scrape(self, html):
        return html

    def parse(self, text, reg):
        pattern = reg.encode('utf8')
        match = re.search(pattern, text, re.UNICODE)
        if match:
            return match.groupdict()
        else:
            return None

    def read(self):
        html = self.download(self.url, self.method, self.data)
        text = self.scrape(html)
        data = self.parse(text, self.reg)
        return data
