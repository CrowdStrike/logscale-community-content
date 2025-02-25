```
// Get UserLogon events for Windows RDP sessions
#event_simpleName=UserLogon event_platform=Win LogonType=10 RemoteAddressIP4=*

// Omit results if the RemoteAddressIP4 field is RFC1819
| !cidr(RemoteAddressIP4, subnet=["224.0.0.0/4", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.1/32", "169.254.0.0/16", "0.0.0.0/32"])

// Create UserName + UserSid Hash
| UserHash:=concat([UserName, UserSid]) | UserHash:=crypto:md5([UserHash])

// Perform initial aggregation; groupBy() will sort by UserHash then LogonTime
| groupBy([UserHash, LogonTime], function=[collect([UserName, UserSid, RemoteAddressIP4, ComputerName, aid])], limit=max)

// Get geoIP for Remote IP
| ipLocation(RemoteAddressIP4)


// Use new neighbor() function to get results for previous row
| neighbor([LogonTime, RemoteAddressIP4, UserHash, RemoteAddressIP4.country, RemoteAddressIP4.lat, RemoteAddressIP4.lon, ComputerName], prefix=prev)

// Make sure neighbor() sequence does not span UserHash values; will occur at the end of a series
| test(UserHash==prev.UserHash)

// Calculate logon time delta in milliseconds from LogonTime to prev.LogonTime and round
| LogonDelta:=(LogonTime-prev.LogonTime)*1000
| LogonDelta:=round(LogonDelta)

// Turn logon time delta from milliseconds to human readable
| TimeToTravel:=formatDuration(LogonDelta, precision=2)

// Calculate distance between Login 1 and Login 2
| DistanceKm:=(geography:distance(lat1="RemoteAddressIP4.lat", lat2="prev.RemoteAddressIP4.lat", lon1="RemoteAddressIP4.lon", lon2="prev.RemoteAddressIP4.lon"))/1000 | DistanceKm:=round(DistanceKm)

// Calculate speed required to get from Login 1 to Login 2
| SpeedKph:=DistanceKm/(LogonDelta/1000/60/60) | SpeedKph:=round(SpeedKph)

// SET THRESHOLD: 1234kph is MACH 1
| test(SpeedKph>1234)

// Format LogonTime Values
| LogonTime:=LogonTime*1000           | formatTime(format="%F %T %Z", as="LogonTime", field="LogonTime")
| prev.LogonTime:=prev.LogonTime*1000 | formatTime(format="%F %T %Z", as="prev.LogonTime", field="prev.LogonTime")

// Make fields easier to read
| Travel:=format(format="%s → %s", field=[prev.RemoteAddressIP4.country, RemoteAddressIP4.country])
| IPs:=format(format="%s → %s", field=[prev.RemoteAddressIP4, RemoteAddressIP4])
| Logons:=format(format="%s → %s", field=[prev.LogonTime, LogonTime])

// Output results to table and sort by highest speed
| table([aid, ComputerName, UserName, UserSid, System, IPs, Travel, DistanceKm, Logons, TimeToTravel, SpeedKph], limit=20000, sortby=SpeedKph, order=desc)

// Express SpeedKph as a value of MACH
| Mach:=SpeedKph/1234 | Mach:=round(Mach)
| Speed:=format(format="MACH %s", field=[Mach])

// Format distance and speed fields to include comma and unit of measure
| format("%,.0f km",field=["DistanceKm"], as="DistanceKm")
| format("%,.0f km/h",field=["SpeedKph"], as="SpeedKph")

// Intelligence Graph; uncomment out one cloud
| rootURL  := "https://falcon.crowdstrike.com/"
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" 
//rootURL  := "https://falcon.eu-1.crowdstrike.com/" 
//rootURL  := "https://falcon.us-2.crowdstrike.com/" 
| format("[Link](%sinvestigate/dashboards/user-search?isLive=false&sharedTime=true&start=7d&user=%s)", field=["rootURL", "UserName"], as="User Search")

// Drop unwanted fields
| drop([Mach, rootURL])
```