---
title: "Parsing and Hunting Failed User Logons in Windows"
date: 2021-03-12
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/m3i45l/20210312_cool_query_friday_parsing_and_hunting/"
mitre: [T1078]
series: Cool Query Friday
---

# Parsing and Hunting Failed User Logons in Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/m3i45l/20210312_cool_query_friday_parsing_and_hunting/](https://www.reddit.com/r/crowdstrike/comments/m3i45l/20210312_cool_query_friday_parsing_and_hunting/) — by Andrew-CS (CrowdStrike) — 2021-03-12

Welcome to our second installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description
```

## Query 2
```cql
| stats count(aid) as failCount earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt values(LocalAddressIP4) as localIP values(aip) as externalIP by aid, ComputerName, UserName, LogonType, SubStatus_hex, Description
```

## Query 3
```cql
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
```

## Query 4
```cql
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```

## Query 5
```cql
event_platform=win event_simpleName=UserLogonFailed2 
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description 
| stats count(aid) as failCount earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt values(LocalAddressIP4) as localIP values(aip) as externalIP by aid, ComputerName, UserName, LogonType, SubStatus_hex, Description 
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```

## Query 6
```cql
| where failCount >= 50
```

## Query 7
```cql
| search LogonType="Terminal Server"
| where failCount >= 50
```

## Query 8
```cql
event_platform=win event_simpleName=UserLogonFailed2 
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description 
| stats count(aid) as failCount dc(aid) as endpointsAttemptedAgainst earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt by RemoteIP 
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```

## Query 9
```cql
event_platform=win event_simpleName=UserLogonFailed2 
| iplocation RemoteIP
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description 
| stats count(aid) as failCount dc(aid) as endpointsAttemptedAgainst earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt by RemoteIP, Country, Region, City 
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```

## Query 10
```cql
event_platform=win event_simpleName=UserLogonFailed2 
| eval SubStatus_hex=tostring(SubStatus_decimal,"hex")
| rename SubStatus_decimal as Status_code_decimal
| lookup local=true LogonType.csv LogonType_decimal OUTPUT LogonType
| lookup local=true win_status_codes.csv Status_code_decimal OUTPUT Description 
| stats count(aid) as failCount dc(aid) as endpointsAttemptedAgainst earliest(ContextTimeStamp_decimal) as firstLogonAttempt latest(ContextTimeStamp_decimal) as lastLogonAttempt by UserName, Description
| eval firstLastDeltaHours=round((lastLogonAttempt-firstLogonAttempt)/60/60,2)
| eval logonAttemptsPerHour=round(failCount/firstLastDeltaHours,0)
| convert ctime(firstLogonAttempt) ctime(lastLogonAttempt)
| sort - failCount
```
