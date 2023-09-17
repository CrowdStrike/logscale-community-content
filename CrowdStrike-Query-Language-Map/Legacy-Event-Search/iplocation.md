Comments: In Legacy Event Search, the function `iplocation` can be provided an IP address for geoip data lookup. Example:

```
event_simpleName=UserLogon LogonType_decimal=10
| iplocation RemoteAddressIP4 
| table _time, aid, RemoteAddressIP4, City, Region, Country
| where isnotnull(Country)
```

in LogScale:

```
#event_simpleName=UserLogon LogonType=10
| iplocation(RemoteAddressIP4) 
| select([_time, aid, RemoteAddressIP4, RemoteAddressIP4.city, RemoteAddressIP4.state, RemoteAddressIP4.country, RemoteAddressIP4.lat, RemoteAddressIP4.lon])
| RemoteAddressIP4.country=*
```

[[CrowdStrike-Query-Language-Map/Legacy-Event-Search/iplocation|iplocation]] 

