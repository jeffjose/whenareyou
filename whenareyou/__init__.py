import csv
import datetime
import os
import requests
from functools import lru_cache
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo


from timezonefinder import TimezoneFinder


LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}'
                '&sensor=false')

airports_csv_path = os.path.join(os.path.dirname(__file__), 'airports.csv')

airports_dict = {}

with open(airports_csv_path, encoding="utf-8") as csvfile:
    airports_reader = csv.DictReader(
        csvfile,
        fieldnames=['id', 'name', 'city', 'country', 'iata', 'icao', 'lat',
                    'lng', 'alt', 'tz', 'dst', 'tz_olson'],
        restkey='info')
    for row in airports_reader:
        airports_dict[row['iata']] = row


@lru_cache(None)
def cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


def get_tz(lat, lng, _tf=TimezoneFinder()):
    tzinfo = _tf.timezone_at(lng=lng, lat=lat)
    if tzinfo:
        return ZoneInfo(tzinfo)
    return None


def whenareyou(address):
    latlong = cached_json_get(
        LONG_LAT_URL.format(quote_plus(address))
    )['results'][0]['geometry']['location']

    return get_tz(latlong['lat'], latlong['lng'])


def whenareyou_apt(airport):
    if not airports_dict[airport]['tz_olson']=='\\N':
        return ZoneInfo(airports_dict[airport]['tz_olson'])

    tzinfo = get_tz(float(airports_dict[airport]['lat']),
                    float(airports_dict[airport]['lng']))
    if tzinfo:
        return tzinfo

    tot_offset = float(airports_dict[airport]['tz'])
    return datetime.timezone(datetime.timedelta(hours=tot_offset),
                             name=(airports_dict[airport]['name'] + ' ' +
                             airports_dict[airport]['city']))



if __name__ == '__main__':
    print("main()")