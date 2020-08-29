import datetime
import json
import os

import requests


class RaspException(Exception):
    pass


def get_rasp(key, station_from, station_to, date, limit=500):
    url = 'https://api.rasp.yandex.net/v3.0/search/?apikey={}&from={}&to={}&date={}&limit={}'.format(key, station_from,
                                                                                                     station_to, date,
                                                                                                     limit)
    response = requests.get(url)
    if response.ok:
        return json.loads(response.text)
    raise RaspException('cannot get yandex rasp info {}'.format(response.text))


def filter_rasp(data: dict, max_diff: int, ignore_express=True):
    max_diff = datetime.timedelta(minutes=max_diff)
    result = []
    for row in data:
        if ignore_express and row.get('thread', {}).get('express_type') is not None:
            continue
        departure = datetime.datetime.fromisoformat(row['departure'])
        now = datetime.datetime.now(departure.tzinfo)
        if now < departure < now + max_diff:
            row['diff'] = departure - now
            result.append(row)
    return result


if __name__ == '__main__':
    key = os.getenv('RASP_KEY')
    station_from = os.getenv('STATION_FROM')
    station_to = os.getenv('STATION_TO')
    date = os.getenv('DATE')
    js = get_rasp(key, station_from, station_to, date)
    js1 = filter_rasp(js['segments'], 60)
    pass
