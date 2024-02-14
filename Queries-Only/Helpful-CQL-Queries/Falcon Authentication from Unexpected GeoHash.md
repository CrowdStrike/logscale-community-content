```
// Get events of interest
EventType=Event_ExternalApiEvent EventType=Event_ExternalApiEvent OperationName=userAuthenticate Success=true
// Get ASN Details
| asn(OriginSourceIpAddress, as=asn)
// Omit ZScaler infra
| asn.org!=/ZSCALER/
//Get IP Location
| ipLocation(OriginSourceIpAddress)
// Get geohash; precision can be adjusted as desired
| geoHash := geohash(lat=OriginSourceIpAddress.lat, lon=OriginSourceIpAddress.lon, precision=2)
// Get RDNS value if available
| rdns(OriginSourceIpAddress, as=rdns)
//Set default values for blank fields
| default(value="Unknown Country", field=[OriginSourceIpAddress.country])
| default(value="Unknown City", field=[OriginSourceIpAddress.city])
| default(value="Unknown ASN", field=[asn.org])
| default(value="Unknown RDNS", field=[rdns])
// Create unified IP details field
| format(format="%s (%s, %s) [%s] - %s", field=[OriginSourceIpAddress, OriginSourceIpAddress.country, OriginSourceIpAddress.city, asn.org, rdns], as=ipDetails)
// Aggregate by UserId and geoHash
| groupBy([UserId, geoHash], function=([count(as=logonCount), min(@timestamp, as=firstLogon), max(@timestamp, as=lastLogon), collect(ipDetails)]))
// Look for geohashes with fewer than 5 logins; can be adjusted as desired
| test(logonCount<5)
// Calculate time delta and determine delta between first and last login
| timeDelta := lastLogon-firstLogon
| formatDuration(timeDelta, from=ms, precision=4, as=timeDelta)
// Format timestamps
| formatTime(format="%Y-%m-%dT%H:%M:%S", field=firstLogon, as="firstLogon")
| formatTime(format="%Y-%m-%dT%H:%M:%S", field=lastLogon, as="lastLogon")
// Create link to geohash map for easier viewing
| format("[Map](https://geohash.softeng.co/%s)", field=geoHash, as=Map)
// Order fields as desired
| select([UserId, firstLogon, lastLogon, logonCount, timeDelta, Map, ipDetails])
```