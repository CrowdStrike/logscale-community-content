---
title: "Scheduled Searches, Failed User Logons, and Thresholds"
date: 2021-10-22
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/qdebwx/20211022_cool_query_friday_scheduled_searches/"
mitre: []
series: Cool Query Friday
---

# Scheduled Searches, Failed User Logons, and Thresholds

> Source: [https://www.reddit.com/r/crowdstrike/comments/qdebwx/20211022_cool_query_friday_scheduled_searches/](https://www.reddit.com/r/crowdstrike/comments/qdebwx/20211022_cool_query_friday_scheduled_searches/) — by Andrew-CS (CrowdStrike) — 2021-10-22

Welcome to our twenty-eighth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
[...]
| search LogonType_decimal IN (2, 7, 10, 13)
```

## Query 2
```cql
[...]
| where ComputerName=LogonDomain
```

## Query 3
```cql
[...]
| table ContextTimeStamp_decimal aid ComputerName LocalAddressIP4 UserName LogonType_decimal RemoteAddressIP4 SubStatus_decimal
```

## Query 4
```cql
index=main sourcetype=UserLogonFailed* event_platform=win event_simpleName=UserLogonFailed2 
| search LogonType_decimal IN (2, 7, 10, 13)
| where ComputerName=LogonDomain
| eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_dgecimal="7", "Unlock", LogonType_decimal="10", "RDP", LogonType_decimal="13", "Unlock Workstation")
| eval SubStatus_decimal=tostring(SubStatus_decimal,"hex")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000064", "User name does not exist")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006A", "User name is correct but the password is wrong")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000234", "User is currently locked out")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000072", "Account is currently disabled")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006F", "User tried to logon outside his day of week or time of day restrictions")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000070", "Workstation restriction, or Authentication Policy Silo violation (look for event ID 4820 on domain controller)")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000193", "Account expiration")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000071", "Expired password")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000133", "Clocks between DC and other computer too far out of sync")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000224", "User is required to change password at next logon")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000225", "Evidently a bug in Windows and not a risk")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xc000015b", "The user has not been granted the requested logon type (aka logon right) at this machine")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006E", "Unknown user name or bad password")
| table ContextTimeStamp_decimal aid ComputerName LocalAddressIP4 UserName LogonType RemoteAddressIP4 SubStatus_decimal
```

## Query 5
```cql
[...]
| stats values(ComputerName) as computerName, values(LocalAddressIP4) as localIPAddresses, count(aid) as failedLogonAttempts, dc(UserName) as credentialsUsed, values(UserName) as userNames, earliest(ContextTimeStamp_decimal) as firstFailedAttmpt, latest(ContextTimeStamp_decimal) as lastFailedAttempt, values(RemoteAddressIP4) as remoteIPAddresses, values(LogonType) as logonTypes, values(SubStatus_decimal) as failedLogonReasons by aid
```

## Query 6
```cql
[...]
| eval failedLoginsDeltaMinutes=round((lastFailedAttempt-firstFailedAttmpt)/60,0)
| eval failedLoginsDeltaSeconds=round((lastFailedAttempt-firstFailedAttmpt),2)
| where failedLogonAttempts>=5
| convert ctime(firstFailedAttmpt) ctime(lastFailedAttempt)
| sort -failedLogonAttempts
```

## Query 7
```cql
index=main sourcetype=UserLogonFailed* event_platform=win event_simpleName=UserLogonFailed2 
| search LogonType_decimal IN (2, 7, 10, 13)
| where ComputerName=LogonDomain
| eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_dgecimal="7", "Unlock", LogonType_decimal="10", "RDP", LogonType_decimal="13", "Unlock Workstation")
| eval SubStatus_decimal=tostring(SubStatus_decimal,"hex")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000064", "User name does not exist")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006A", "User name is correct but the password is wrong")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000234", "User is currently locked out")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000072", "Account is currently disabled")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006F", "User tried to logon outside his day of week or time of day restrictions")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000070", "Workstation restriction, or Authentication Policy Silo violation (look for event ID 4820 on domain controller)")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000193", "Account expiration")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000071", "Expired password")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000133", "Clocks between DC and other computer too far out of sync")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000224", "User is required to change password at next logon")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC0000225", "Evidently a bug in Windows and not a risk")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xc000015b", "The user has not been granted the requested logon type (aka logon right) at this machine")
| eval SubStatus_decimal=replace(SubStatus_decimal,"0xC000006E", "Unknown user name or bad password")
| stats values(ComputerName) as computerName, values(LocalAddressIP4) as localIPAddresses, count(aid) as failedLogonAttempts, dc(UserName) as credentialsUsed, values(UserName) as userNames, earliest(ContextTimeStamp_decimal) as firstFailedAttmpt, latest(ContextTimeStamp_decimal) as lastFailedAttempt, values(RemoteAddressIP4) as remoteIPAddresses, values(LogonType) as logonTypes, values(SubStatus_decimal) as failedLogonReasons by aid
| eval failedLoginsDeltaMinutes=round((lastFailedAttempt-firstFailedAttmpt)/60,0)
| eval failedLoginsDeltaSeconds=round((lastFailedAttempt-firstFailedAttmpt),2)
| where failedLogonAttempts>=5
| convert ctime(firstFailedAttmpt) ctime(lastFailedAttempt)
| sort -failedLogonAttempts
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
index=main sourcetype=AgentConnect* event_simpleName=AgentConnect 
| fields aip, aid, ConnectTime_decimal 
| stats latest(aip) as aip latest(ConnectTime_decimal) as connectionTime by aid
| iplocation aip 
| lookup local=true aid_master aid OUTPUT ComputerName 
| table aid, ComputerName, connectionTime, aip, Country, Region, City
| convert ctime(connectionTime)
| rename aid as "Falcon ID", ComputerName as "Endpoint", connectionTime as "Last Connection", aip as "Last External IP"
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] Nerdcentric:** When I test the query it is defaulting back to a search window of "Last 15 minutes". If I am scheduling this to run once every 24 hours, am I only getting the events for the last 15 minutes when it runs? I feel like I missed where you set the search window to 24 hours. Or is that automatic based on …

**A — [CS] Andrew-CS:** Great question. When you click "Schedule Query" the frequency you pick will also be the search window.

**Q — [Community] DreadlockedSOC:** I'm a little late to this party. How do I set my every 24hr scheduled search to query the last 7 days of data? I want my query to grab the last 7 days of data every 24hrs. I tried to add 'earliest -7d' but it barked an error at me.

**A — [CS] Andrew-CS:** At present, 24 hours is the max you can set as we need to assess how ~~soul crushing~~ performant the queries are :)

**Q — [Community] Ballzovsteel:** When I am looking at the delta and delta seconds. What does that exactly mean, is that the time between attempts?

**A — [CS] Andrew-CS:** It’s the time difference between the very first failed login and the very last failed login. So if there were 10 failed attempts, it would be the difference between 1 and 10.
