import csv
import datetime
import os
import requests

from functools import lru_cache
from urllib.parse import quote#, quote_plus
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

# -----------------------------------------------------------------------------
# old / broken: using google maps api to obtain address lat/lng
# -----------------------------------------------------------------------------
_LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}'
                 '&sensor=false')
# -----------------------------------------------------------------------------
# alternative: use openstreetmap
# -----------------------------------------------------------------------------
_LONG_LAT_URL_Nominatim = "http://nominatim.openstreetmap.org/search?q="
# -----------------------------------------------------------------------------


# HELPERS ---------------------------------------------------------------------
@lru_cache(None)
def _cached_json_get(url):
    """
    a general helper -
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()

def _queryOSM(address):
    """
    a helper to query nominatim.openstreetmap for given address
    """
    url = _LONG_LAT_URL_Nominatim + quote(address) + '&format=json&polygon=0'
    response = _cached_json_get(url)[0]
    return (float(response.get(key)) for key in ('lat', 'lon'))

def _get_tz(lat, lng, _tf=TimezoneFinder()):
    """
    a helper to call timezonefinder
    """
    tzinfo = _tf.timezone_at(lng=lng, lat=lat)
    if tzinfo:
        return ZoneInfo(tzinfo)
    return None


# MAIN METHODS ----------------------------------------------------------------
def whenareyou(address):
    """
    Find the time zone of a given address

    Parameters
    ----------
    address : str
        address to search.

    Returns
    -------
    tzinfo
        zoneinfo.ZoneInfo

    """
    # latlong = _cached_json_get(
    #     _LONG_LAT_URL.format(quote_plus(address))
    # )['results'][0]['geometry']['location']

    return _get_tz(*_queryOSM(address))#latlong['lat'], latlong['lng'])



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


def whenareyou_IATA(airport):
    """
    Find the time zone of a given airport IATA code

    Parameters
    ----------
    airport : str
        airport IATA code.

    Returns
    -------
    tzinfo
        datetime.timezone or zoneinfo.ZoneInfo

    """
    airport = airport.upper()
    # if not _airports_dict[airport]['tz_olson']=='\\N':
    #     return ZoneInfo(_airports_dict[airport]['tz_olson'])

    tzinfo = _get_tz(float(_airports_dict[airport]['lat']),
                     float(_airports_dict[airport]['lng']))
    if tzinfo:
        return tzinfo

    tot_offset = float(_airports_dict[airport]['tz'])
    return datetime.timezone(datetime.timedelta(hours=tot_offset),
                             name=(_airports_dict[airport]['name'] + ' ' +
                             _airports_dict[airport]['city']))