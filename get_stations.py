import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ns_tool.settings')
import django

django.setup()

import requests
import json
sys.path.insert(0, 'pricing')
from pricing.models import Station
import pricing.data as d

def fetch_stations():
    e = requests.get(d.req_url, headers=d.app_headers)
    data = json.loads(e.text)
    station_data_list = data['payload']
    return station_data_list


def reset_db():
    station_list = []
    for entry in fetch_stations():
        if entry['land'] != 'NL':
            continue
        kwargs = {'code': entry['code'], 'latitude': entry['lat'], 'longitude': entry['lng'],
                  'short': entry['namen']['kort'], 'medium': entry['namen']['middel'], 'long': entry['namen']['lang']}
        station_list.append(Station(**kwargs))
    Station.objects.bulk_create(station_list)


if __name__ == '__main__':
    reset_db()
