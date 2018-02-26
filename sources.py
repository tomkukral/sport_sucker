#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from stravalib import Client
from scrapers import RegexpScraper
from pprint import pprint

import datetime
import pytz
import re

class Strava(object):
    def __init__(self, cfg):
        self.token = cfg.get('token')
        self.convert_swim = cfg.get('convert_swim')

        self.client = Client(access_token=self.token)
        self.athlete = self.client.get_athlete()
        self.activities = self.client.get_activities()

        print('Loading data for: {} {}'.format(self.athlete.firstname.encode('utf8'), self.athlete.lastname.encode('utf8')))

    def json(self):
        out = []

        for a in self.activities:
            out.append(self._format_activity(a))

        return out

    def _format_activity(self, a):
        out = {
            'measurement': 'activity',
            'time': a.start_date.isoformat(),
            'fields': {
                'distance': a.distance.num,
                'moving_time': a.moving_time.total_seconds(),
                'elapsed_time': a.elapsed_time.total_seconds(),
                'total_elevation_gain': a.total_elevation_gain.num,
            },
            'tags': {
                'type': a.type,
                'athlete': a.athlete.id,
            },
        }

        return out

    def _get_param_from_activity(self, a):
        return {
            'name': a.name,
            'activity_type': a.type,
            'start_date_local': a.start_date_local.isoformat(),
            'elapsed_time': int(a.elapsed_time.total_seconds()),
            'description': a.description,
            'distance': a.distance,
            'private': a.private,
        }

    def convert_swimming(self):
        print(self.convert_swim)

        lap_time_min = self.convert_swim['lap_time_min']
        lap_time_max = self.convert_swim['lap_time_max']
        lap_distance = self.convert_swim['lap_distance']

        for a in self.activities:
            if a.type == 'Swim' and a.distance.num == 0 and not a.description and not re.match('DELETE:.*', a.name):
                print(self._format_activity(a))

                problem = 0
                distance = 0
                # count laps and distances
                for lap in a.laps:
                    if lap_time_min < lap.elapsed_time.total_seconds() < lap_time_max:
                        distance += lap_distance
                    else:
                        problem += 1
                        break

                if problem == 0 and distance > 0:
                    print('Fine:')

                    new_activity = self._get_param_from_activity(a)
                    new_activity['distance'] = float(distance)

                    if not new_activity['description']:
                        new_activity['description'] = 'Converted by Sport Sucker.\nActivity #{}'.format(a.id)

                    print('Create new')
                    print(new_activity)

                    new_activity_saved = self.client.create_activity(**new_activity)

                    if not a.description:
                        self.client.update_activity(
                            a.id,
                            name='DELETE: {}'.format(a.name),
                            description='Should be deleted, replaced by #{}'.format(new_activity_saved.id)
                        )

                else:
                    print('UNABLE to convert swimming')



class SwimmingPools(object):
    def __init__(self, cfg):
        self.pools = cfg

    def json(self):
        out = []

        for k, v in self.pools.items():
            a = RegexpScraper(**v)
            fields = a.read()

            if fields:
                out.append({
                    "measurement": "people",
                    "tags": {
                        "location": k,
                    },
                    "time": datetime.datetime.now(tz=pytz.UTC).isoformat(),
                    "fields": {k: int(v) for (k, v) in fields.items()}
                })
            else:
                print('No fields from {}'.format(k.encode('utf8')))

        return out

