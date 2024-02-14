[Reddit Link](https://www.reddit.com/r/crowdstrike/comments/149krol/20230614_cool_query_friday_watching_the_watchers/)


```
// Get successful Falcon console logins
EventType=Event_ExternalApiEvent OperationName=userAuthenticate Success=true

// Get ASN Details for OriginSourceIpAddress
| asn(OriginSourceIpAddress, as=asn)

// Omit ZScaler infra
| asn.org!=/ZSCALER/

//Get IP Location for OriginSourceIpAddress
| ipLocation(OriginSourceIpAddress)

// Get geohash with precision of 2; precision can be adjusted as desired
| geohash(lat=OriginSourceIpAddress.lat, lon=OriginSourceIpAddress.lon, precision=2, as=geohash)

// Get RDNS value, if available, for OriginSourceIpAddress
| rdns(OriginSourceIpAddress, as=rdns)

//Set default values for blank fields
| default(value="Unknown Country", field=[OriginSourceIpAddress.country])
| default(value="Unknown City", field=[OriginSourceIpAddress.city])
| default(value="Unknown ASN", field=[asn.org])
| default(value="Unknown RDNS", field=[rdns])

// Create unified IP details field for easier viewing
| format(format="%s (%s, %s) [%s] - %s", field=[OriginSourceIpAddress, OriginSourceIpAddress.country, OriginSourceIpAddress.city, asn.org, rdns], as=ipDetails)

// Aggregate details by UserId and geoHash
| groupBy([UserId, geoHash], function=([count(as=logonCount), min(@timestamp, as=firstLogon), max(@timestamp, as=lastLogon), collect(ipDetails)]))

// Look for geohashes with fewer than 5 logins; logonCount can be adjusted as desired
| test(logonCount<5)

// Calculate time delta and determine span between first and last login
| timeDelta := lastLogon-firstLogon
| formatDuration(timeDelta, from=ms, precision=4, as=timeDelta)

// Format timestamps
| formatTime(format="%Y-%m-%dT%H:%M:%S", field=firstLogon, as="firstLogon")
| formatTime(format="%Y-%m-%dT%H:%M:%S", field=lastLogon, as="lastLogon")

// Create link to geohash map for easy cartography
| format("[Map](https://geohash.softeng.co/%s)", field=geoHash, as=Map)

// Order fields as desired
| select([UserId, firstLogon, lastLogon, timeDelta, logonCount, Map, ipDetails])
```

[[regex]] | [[asn]] | [[ipLocation]] | [[geoHash]] | [[rdns]] | [[default]] | [[format - concat]] | [[groupBy]] | [[test]] | [[formatDuration]] | [[formatTime]] | [[format - hyperlinks]] | [[select]]
