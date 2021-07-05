import csv
import datetime
import os
import requests
from functools import lru_cache
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo


from timezonefinder import TimezoneFinder


_LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}'
                '&sensor=false')

_airports_dict = {}
with open(os.path.join(os.path.dirname(__file__), 'airports.csv'), encoding="utf-8") as csvfile:
    airports_reader = csv.DictReader(
        csvfile,
        fieldnames=['id', 'name', 'city', 'country', 'iata', 'icao', 'lat',
                    'lng', 'alt', 'tz', 'dst', 'tz_olson'],
        restkey='info')
    for row in airports_reader:
        _airports_dict[row['iata']] = row
del airports_reader, csvfile, row


@lru_cache(None)
def _cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


def _get_tz(lat, lng, _tf=TimezoneFinder()):
    tzinfo = _tf.timezone_at(lng=lng, lat=lat)
    if tzinfo:
        return ZoneInfo(tzinfo)
    return None


def whenareyou(address):
    latlong = _cached_json_get(
        _LONG_LAT_URL.format(quote_plus(address))
    )['results'][0]['geometry']['location']

    return _get_tz(latlong['lat'], latlong['lng'])


def whenareyou_apt(airport):
    if not _airports_dict[airport]['tz_olson']=='\\N':
        return ZoneInfo(_airports_dict[airport]['tz_olson'])

    tzinfo = _get_tz(float(_airports_dict[airport]['lat']),
                    float(_airports_dict[airport]['lng']))
    if tzinfo:
        return tzinfo

    tot_offset = float(_airports_dict[airport]['tz'])
    return datetime.timezone(datetime.timedelta(hours=tot_offset),
                             name=(_airports_dict[airport]['name'] + ' ' +
                             _airports_dict[airport]['city']))