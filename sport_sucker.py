#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from scrapers import PoolScraper
from influxdb import InfluxDBClient
from pprint import pprint

import datetime
import json
import pytz
import yaml

def main():
    # load configuration
    with open('config.yml') as f:
        try:
            cfg = yaml.load(f)
        except AttributeError:
            print('Failed to load config.yml')
            raise

    pprint(cfg)


    client = InfluxDBClient(**cfg['export']['mqtt'])
    client.create_database('sport_sucker')
    client.switch_database('sport_sucker')

    json_body = []

    for k, v in sources['swimming_pools'].items():
        print(k)
        a = PoolScraper(**v)
        fields = a.read()

        if fields:
            json_body.append({
                    "measurement": "people",
                    "tags": {
                        "location": k,
                    },
                    "time": datetime.datetime.now(tz=pytz.UTC).isoformat(),
                    "fields": {k: int(v) for (k, v) in fields.items()}
                })


    # send datapoints
    pprint(json_body)
    client.write_points(json_body)

if __name__ == '__main__':
    main()
