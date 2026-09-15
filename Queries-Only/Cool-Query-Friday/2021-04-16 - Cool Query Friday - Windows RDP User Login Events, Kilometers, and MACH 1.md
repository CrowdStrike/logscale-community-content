---
title: "Windows RDP User Login Events, Kilometers, and MACH 1"
date: 2021-04-16
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ms2mlz/20210416_cool_query_friday_windows_rdp_user_login/"
mitre: []
series: Cool Query Friday
---

# Windows RDP User Login Events, Kilometers, and MACH 1

> Source: [https://www.reddit.com/r/crowdstrike/comments/ms2mlz/20210416_cool_query_friday_windows_rdp_user_login/](https://www.reddit.com/r/crowdstrike/comments/ms2mlz/20210416_cool_query_friday_windows_rdp_user_login/) — by Andrew-CS (CrowdStrike) — 2021-04-16

Welcome to our seventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win event_simpleName=UserLogon
| eval LogonType=case(LogonType_decimal="2", "Local Logon", LogonType_decimal="3", "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", LogonType_decimal="6", "Proxy", LogonType_decimal="7", "Unlock", LogonType_decimal="8", "Network Cleartext", LogonType_decimal="9", "New Credentials", LogonType_decimal="10", "RDP", LogonType_decimal="11", "Cached Credentials", LogonType_decimal="12", "Auditing", LogonType_decimal="13", "Unlock Workstation")
```

## Query 2
```cql
event_platform=win event_simpleName=UserLogon LogonType_decimal=10
| iplocation RemoteIP
```

## Query 3
```cql
event_platform=win event_simpleName=UserLogon LogonType_decimal=10 (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP
| stats values(UserName) as userNames dc(UserSid_readable) as userAccountsUsed count(UserSid_readable) as successfulLogins dc(Country) as countriesFrom by ComputerName, aid
| sort - successfulLogins
```

## Query 4
```cql
| stats values(UserName) as userNames dc(UserSid_readable) as userAccountsUsed count(UserSid_readable) as successfulLogins dc(Country) as countriesCount by ComputerName, aid
| sort - successfulLogins
```

## Query 5
```cql
event_platform=win event_simpleName=UserLogon LogonType_decimal=10 (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP
| where Country!="United States"
| stats values(UserName) as userNames dc(UserSid_readable) as userAccountsUsed count(UserSid_readable) as successfulLogins values(Country) as countriesFrom dc(Country) as countriesCount by ComputerName, aid
| sort - successfulLogins
```

## Query 6
```cql
event_platform=win event_simpleName=UserLogon LogonType_decimal=10 (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP
| stats dc(aid) as systemsAccessed count(UserSid_readable) as totalRDPLogins values(Country) as countriesFrom dc(Country) as countriesCount by UserName, UserSid_readable
| sort - totalRDPLogins
```

## Query 7
```cql
event_platform=win event_simpleName=UserLogon LogonType_decimal=10 ProductType=1 (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP
| stats dc(aid) as systemsAccessed count(UserSid_readable) as totalRDPLogins values(Country) as countriesFrom dc(Country) as countriesCount by UserName, UserSid_readable
| sort - totalRDPLogins
```

## Query 8
```cql
| inputlookup aid_master 
| eval ProductTypeName=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
| stats values(Version) as osVersions by ProductType, ProductTypeName
```

## Query 9
```cql
event_platform=win event_simpleName=UserLogon (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP
```

## Query 10
```cql
| stats earliest(LogonTime_decimal) as firstLogon earliest(lat) as lat1 earliest(lon) as lon1 earliest(Country) as country1 earliest(Region) as region1 earliest(City) as city1 latest(LogonTime_decimal) as lastLogon latest(lat) as lat2 latest(lon) as lon2 latest(Country) as country2 latest(Region) as region2 latest(City) as city2 dc(RemoteIP) as remoteIPCount by UserSid_readable, UserName
```

## Query 11
```cql
| where remoteIPCount > 1
```

## Query 12
```cql
| eval timeDelta=round((lastLogon-firstLogon)/60/60,2)
```

## Query 13
```cql
| eval rlat1 = pi()*lat1/180, rlat2=pi()*lat2/180, rlat = pi()*(lat2-lat1)/180, rlon= pi()*(lon2-lon1)/180
| eval a = sin(rlat/2) * sin(rlat/2) + cos(rlat1) * cos(rlat2) * sin(rlon/2) * sin(rlon/2) 
| eval c = 2 * atan2(sqrt(a), sqrt(1-a)) 
| eval distance = round((6371 * c),0)
```

## Query 14
```cql
| eval speed=round((distance/timeDelta),2)
```

## Query 15
```cql
| table UserSid_readable, UserName, firstLogon, country1, region1, city1, lastLogon, country2, region2, city2, timeDelta, distance, speed remoteIPCount
| convert ctime(firstLogon), ctime(lastLogon)
| sort - speed
```

## Query 16
```cql
| rename UserSid_readable AS "User SID", UserName AS User, firstLogon AS "First Logon Time", country1 AS " First Country" region1 AS "First Region", city1 AS "First City", lastLogon AS "Last Logon Time", country2 AS "Last Country", region2 AS "Last Region", city2 AS "Last City", timeDelta AS "Elapsed Time (hours) ", distance AS "Kilometers Between GeoIP Locations", speed AS "Required Speed (km/h)", remoteIPCount as "Number of Remote Logins"
```

## Query 17
```cql
event_platform=win event_simpleName=UserLogon (RemoteIP!=172.16.0.0/12 AND RemoteIP!=192.168.0.0/16 AND RemoteIP!=10.0.0.0/8)
| iplocation RemoteIP 
| stats earliest(LogonTime_decimal) as firstLogon earliest(lat) as lat1 earliest(lon) as lon1 earliest(Country) as country1 earliest(Region) as region1 earliest(City) as city1 latest(LogonTime_decimal) as lastLogon latest(lat) as lat2 latest(lon) as lon2 latest(Country) as country2 latest(Region) as region2 latest(City) as city2 dc(RemoteIP) as remoteIPCount by UserSid_readable, UserName
| where remoteIPCount > 1
| eval timeDelta=round((lastLogon-firstLogon)/60/60,2)
| eval rlat1 = pi()*lat1/180, rlat2=pi()*lat2/180, rlat = pi()*(lat2-lat1)/180, rlon= pi()*(lon2-lon1)/180
| eval a = sin(rlat/2) * sin(rlat/2) + cos(rlat1) * cos(rlat2) * sin(rlon/2) * sin(rlon/2) 
| eval c = 2 * atan2(sqrt(a), sqrt(1-a)) 
| eval distance = round((6371 * c),0)
| eval speed=round((distance/timeDelta),2)
| table UserSid_readable, UserName, firstLogon, country1, region1, city1, lastLogon, country2, region2, city2, timeDelta, distance, speed remoteIPCount
| convert ctime(firstLogon), ctime(lastLogon)
| sort - speed
| rename UserSid_readable AS "User SID", UserName AS User, firstLogon AS "First Logon Time", country1 AS " First Country" region1 AS "First Region", city1 AS "First City", lastLogon AS "Last Logon Time", country2 AS "Last Country", region2 AS "Last Region", city2 AS "Last City", timeDelta AS "Elapsed Time (hours) ", distance AS "Kilometers Between GeoIP Locations", speed AS "Required Speed (km/h)", remoteIPCount as "Number of Remote Logins"
```

## Query 18
```cql
[...]
| eval speed=round((distance/timeDelta),2)
| where speed > 1234
[...]
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] Affectionate_Will487:** In an environment that allows RDP how would you narrow down to find either a system with let’s say 100 failures on let’s say 100 hosts something like that , or a system that doesn’t use rdp and now all over sudden using rdp, or what are some strange patterns to look for ?

**A — [CS] Andrew-CS:** You want to check failed user logins. CQF here: https://www.reddit.com/r/crowdstrike/comments/m3i45l/20210312\_cool\_query\_friday\_parsing\_and\_hunting/

**Q — [Community] cs-del:** I have a similar scheduled search for my environment monitoring successful RDP connections (logon type 10) originating from external IP address. This is one of the areas that client is mainly interested in. One of the detection from that search is user logon event that shows up a remote IP on client …

**A — [CS] Andrew-CS:** Hi there. In Process Explorer, you're only seeing outbound network connections. You can look for the event `NetworkReceiveAcceptIP4`. Authentications will always be pinned to LSASS as that handles auth for Windows systems.
