whenareyou
==========

Gets the time zone of any location in the world.

This fork is a modified version of @sils [whenareyou](https://github.com/aerupt/whenareyou). Uses `nominatim.openstreetmap.org` to search the location. It caches the results so that the server isn't stressed by repeated queries of the same address.

## example usage

```Python
from whenareyou import whenareyou

tz = whenareyou('Hamburg')

tz
Out[3]: zoneinfo.ZoneInfo(key='Europe/Berlin')

from datetime import datetime

datetime(2002, 10, 27, 6, 0, 0, tzinfo=tz)
Out[5]: datetime.datetime(2002, 10, 27, 6, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Berlin'))

datetime(2002, 10, 27, 6, 0, 0, tzinfo=tz).isoformat()
Out[6]: '2002-10-27T06:00:00+01:00'
```
Lookup of IATA airport codes (3-letter) is also included:
```Python
from whenareyou import whenareyou_IATA

whenareyou_IATA('PVG') # Shanghai Pudong
Out[8]: zoneinfo.ZoneInfo(key='Asia/Shanghai')
```

### requires
- Python 3.9+
- [requests](https://pypi.org/project/requests/), [timezonefinder](https://pypi.org/project/timezonefinder/)
