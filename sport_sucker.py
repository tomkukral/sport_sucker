#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
from pprint import pprint
from stravalib import Client

from sources import Strava
from sources import SwimmingPools

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
    json_body = []

    # strava
    if cfg.get('sources', {}).get('strava', False):
        c = Strava(cfg['sources']['strava'])

        # convert swim
        if cfg.get('sources', {}).get('strava', {}).get('convert_swim'):
            c.convert_swimming()

        # export
        if cfg.get('sources', {}).get('strava', {}).get('token', None):
            json_body += (c.json())

    # swimming pools
    if cfg.get('sources', {}).get('swimming_pools', False):
        c = SwimmingPools(cfg['sources']['swimming_pools'])
        json_body += c.json()

    if json_body:
        # send datapoints
        client = InfluxDBClient(**cfg['export']['influxdb'])
        client.switch_database('sport_sucker')
        pprint(json_body)
        client.write_points(json_body)

if __name__ == '__main__':
    main()
