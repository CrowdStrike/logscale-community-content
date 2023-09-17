The `geoHash` function calculates a geohash value given two fields representing latitude and longitude. Precision can be set from to values from 1 (least precise) to 12 (most precise).

```
| geoHash := geohash(lat=OriginSourceIpAddress.lat, lon=OriginSourceIpAddress.lon, precision=2)
```

[geoHash Documentation](https://library.humio.com/data-analysis/functions-geohash.html) | [geohash information (Wikipedia)](https://en.wikipedia.org/wiki/Geohash)

