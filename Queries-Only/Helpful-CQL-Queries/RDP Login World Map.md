```
#event_simpleName=UserLogon LogonType=10

| RemoteAddressIP4 = *
| ipLocation(RemoteAddressIP4)
| worldMap(lat=RemoteAddressIP4.lat, lon=RemoteAddressIP4.lon, magnitude=count(aid))

```