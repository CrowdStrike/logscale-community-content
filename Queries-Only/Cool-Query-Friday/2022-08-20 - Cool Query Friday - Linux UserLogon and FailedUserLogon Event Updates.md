---
title: "Linux UserLogon and FailedUserLogon Event Updates"
date: 2022-08-20
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/wta83n/20220820_cool_query_friday_linux_userlogon_and/"
mitre: []
series: Cool Query Friday
---

# Linux UserLogon and FailedUserLogon Event Updates

> Source: [https://www.reddit.com/r/crowdstrike/comments/wta83n/20220820_cool_query_friday_linux_userlogon_and/](https://www.reddit.com/r/crowdstrike/comments/wta83n/20220820_cool_query_friday_linux_userlogon_and/) — by Andrew-CS (CrowdStrike) — 2022-08-20

Welcome to our forty-seventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
[...]
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
```

## Query 2
```cql
[...]
| iplocation RemoteAddressIP4
```

## Query 3
```cql
event_platform=Lin event_simpleName IN (UserLogon, UserLogonFailed2) LogonType_decimal=10
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
| iplocation RemoteAddressIP4
| stats count(aid) as loginAttempts, dc(aid) as totalSystemsTargeted, values(ComputerName) as computersTargeted, values(UserName) as accountsTargeted by RemoteAddressIP4, Country, Region, City
| sort - loginAttempts
```

## Query 4
```cql
event_platform=Lin event_simpleName IN (UserLogon, UserLogonFailed2) LogonType_decimal=10
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
| iplocation RemoteAddressIP4
| stats count(aid) as loginAttempts, dc(aid) as totalSystemsTargeted, values(ComputerName) as computersTargeted by UserName, RemoteAddressIP4, Country, Region, City
| sort - loginAttempts
```

## Query 5
```cql
event_platform=Lin event_simpleName IN (UserLogon, UserLogonFailed2) LogonType_decimal=10
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
| iplocation RemoteAddressIP4
| stats count(aid) as loginAttempts, dc(aid) as totalSystemsTargeted, dc(RemoteAddressIP4) as remoteIPsInvolved, values(Country) as countriesInvolved, values(ComputerName) as computersTargeted by UserName
| sort - loginAttempts
```

## Query 6
```cql
event_platform=Lin event_simpleName IN (UserLogon) 
| iplocation RemoteAddressIP4
| convert ctime(LogonTime_decimal) as LogonTime, ctime(PasswordLastSet_decimal) as PasswordLastSet
| eval LogonType=case(LogonType_decimal=2, "Interactive", LogonType_decimal=10, "Remote Interactive/SSH")
| eval UserIsAdmin=case(UserIsAdmin_decimal=1, "Admin", UserIsAdmin_decimal=0, "Non-Admin")
| fillnull value="-" RemoteAddressIP4, Country, Region, City
| table aid, ComputerName, UserName, UID_decimal, PasswordLastSet, UserIsAdmin, LogonType, LogonTime, RemoteAddressIP4, Country, Region, City 
| sort 0 +ComputerName, LogonTime
| rename aid as "Agent ID", ComputerName as "Endpoint", UserName as "User", UID_decimal as "User ID", PasswordLastSet as "Password Last Set", UserIsAdmin as "Admin?", LogonType as "Logon Type", LogonTime as "Logon Time", RemoteAddressIP4 as "Remote IP", Country as "GeoIP Country", City as "GeoIP City", Region as "GeoIP Region"
```

## Query 7
```cql
| convert ctime(LogonTime_decimal) as LogonTime, ctime(PasswordLastSet_decimal) as PasswordLastSet
| eval LogonType=case(LogonType_decimal=2, "Interactive", LogonType_decimal=10, "Remote Interactive/SSH")
| eval UserIsAdmin=case(UserIsAdmin_decimal=1, "Admin", UserIsAdmin_decimal=0, "Non-Admin")
```

## Query 8
```cql
event_simpleName=UserLogon NOT RemoteIP IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
| iplocation RemoteIP 
| eval userID=coalesce(UserSid_readable, UID_decimal)
| eval stream1=mvzip(mvzip(mvzip(mvzip(mvzip(LogonTime_decimal, lat, ":::"), lon, ":::"), Country, ":::"), Region, ":::"), City, ":::")
| stats values(stream1) as stream2, dc(RemoteIP) as remoteIPCount by userID, UserName, event_platform
| where remoteIPCount > 1 
| fields userID UserName event_platform stream2
| mvexpand stream2
| eval stream1=split(stream2, ":::")
| eval LogonTime=mvindex(stream1, 0)
| eval lat=mvindex(stream1, 1)
| eval lon=mvindex(stream1, 2)
| eval country=mvindex(stream1, 3)
| eval region=mvindex(stream1, 4)
| eval city=mvindex(stream1, 5)
| sort - userID + LogonTime
| streamstats values(LogonTime) as previous_logon, values(lat) as previous_lat, values(lon) as previous_lon, values(country) as previous_country, values(region) as previous_region, values(city) as previous_city by userID UserName event_platform current=f window=1 reset_on_change=true
| fillnull value="Initial"
| eval timeDelta=round((LogonTime-previous_logon)/60/60,2)
| eval rlat1 = pi()*previous_lat/180, rlat2=pi()*lat/180, rlat = pi()*(lat-previous_lat)/180, rlon= pi()*(lon-previous_lon)/180
| eval a = sin(rlat/2) * sin(rlat/2) + cos(rlat1) * cos(rlat2) * sin(rlon/2) * sin(rlon/2) 
| eval c = 2 * atan2(sqrt(a), sqrt(1-a)) 
| eval distance = round((6371 * c),0)
| eval speed=round((distance/timeDelta),2) 
| fields - stream1 stream2 
| where previous_logon!="Initial" AND speed > 1234
| table event_platform UserName userID previous_logon previous_country previous_region previous_city LogonTime country region city distance timeDelta speed
| sort - speed
| convert ctime(previous_logon) ctime(LogonTime)
| rename event_platform as "Platform", UserName AS "User", userID AS "User ID", previous_logon AS "Logon", previous_country AS Country, previous_region AS "Region", previous_city AS City, LogonTime AS "Next Logon", country AS "Next Country", region AS "Next Region", city AS "Next City", distance AS Distance, timeDelta AS "Time Delta", speed AS "Required Speed (km\h)"
```

## Query 9
```cql
| where previous_logon!="Initial" AND speed > 1234
```
