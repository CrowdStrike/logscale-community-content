---
title: "Mining Windows CommandHistory for Artifacts"
date: 2021-10-15
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/q8qzmp/20211015_cool_query_friday_mining_windows/"
mitre: []
series: Cool Query Friday
---

# Mining Windows CommandHistory for Artifacts

> Source: [https://www.reddit.com/r/crowdstrike/comments/q8qzmp/20211015_cool_query_friday_mining_windows/](https://www.reddit.com/r/crowdstrike/comments/q8qzmp/20211015_cool_query_friday_mining_windows/) — by Andrew-CS (CrowdStrike) — 2021-10-15

Welcome to our twenty-seventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
index=main sourcetype=CommandHistory* event_platform=win event_simpleName=CommandHistory
| rex field=CommandHistory ".*(?<passedURL>http(|s)\:\/\/.*\.(net|com|org|io)).*"
```

## Query 2
```cql
http(s):\\<anything>.com|.net|.org|.io
```

## Query 3
```cql
index=main sourcetype=CommandHistory* event_platform=win event_simpleName=CommandHistory
| rex field=CommandHistory ".*(?<passedURL>http(|s)\:\/\/.*\.(net|com|org|io)).*"
| where isnotnull(passedURL)
```

## Query 4
```cql
[...]
| fillnull ApplicationName value="powershell.exe"
| eval timestamp=timestamp/1000
| table timestamp ComputerName ApplicationName TargetProcessId_decimal passedURL CommandHistory 
| convert ctime(timestamp)
| rename timestamp as Time, ComputerName as Endpoint, ApplicationName as "Responsible Application", TargetProcessId_decimal as "Falcon PID", passedURL as "URL Fragment", CommandHistory as "Complete Command Context"
```

## Query 5
```cql
[...]
| table timestamp ComputerName ApplicationName TargetProcessId_decimal passedURL CommandHistory 
| search ComputerName!=DESKTOP-ICAKMS8 AND passedURL!="*.crowdstrike.*" AND passedURL!="*.microsoft.*"
| convert ctime(timestamp)
[...]
```

## Query 6
```cql
index=main sourcetype=CommandHistory* event_platform=win event_simpleName=CommandHistory
| rex field=CommandHistory ".*(?<passedURL>http(|s)\:\/\/.*\.(net|com|org|io)).*"
| where isnotnull(passedURL)
| fillnull ApplicationName value="powershell.exe"
| eval timestamp=timestamp/1000
| table timestamp ComputerName ApplicationName TargetProcessId_decimal passedURL CommandHistory 
| search ComputerName!=DESKTOP-ICAKMS8 AND passedURL!="*.crowdstrike.*" AND passedURL!="*.microsoft.*"
| convert ctime(timestamp)
| rename timestamp as Time, ComputerName as Endpoint, ApplicationName as "Responsible Application", TargetProcessId_decimal as "Falcon PID", passedURL as "URL Fragment", CommandHistory as "Complete Command Context"
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
index=main AND (sourcetype=CommandHistory* event_platform=win event_simpleName=CommandHistory) OR (sourcetype=ProcessRollup* event_platform=win event_simpleName=ProcessRollup2) | rex field=CommandHistory ".(?<passedURL>http(|s)://..(net|com|org|io)).*" | stats dc(event_simpleName) as eventCount, values(ComputerName) as ComputerName, values(FileName) as FileName, values(UserSid_readable) as UserSid_readable, values(CommandHistory) as CommandHistory, values(passedURL) as passedURL, latest(ProcessStartTime_decimal) as time by aid, TargetProcessId_decimal | where eventCount>1 AND isnotnull(passedURL) | lookup local=true userinfo.csv UserSid_readable OUTPUT UserName | table time aid ComputerName UserSid_readable UserName FileName TargetProcessId_decimal passedURL CommandHistory | sort + time | convert ctime(time) | rename time as Time, aid as "Falcon Agent ID", ComputerName as Endpoint, UserSid_readable as "User SID", UserName as User, FileName as File, TargetProcessId_decimal as "Falcon PID", passedURL as "URL", CommandHistory as "Complete Command History"
```
— [CS] Andrew-CS · comment score 4

### Q&A

**Q — [Community] Sackman_and_Throbbin:** Is there a way to query the parent process data to determine UserName info?

**A — [CS] Andrew-CS:** Hi there. Try this: index=main AND (sourcetype=CommandHistory* event_platform=win event_simpleName=CommandHistory) OR (sourcetype=ProcessRollup* event_platform=win event_simpleName=ProcessRollup2) | rex field=CommandHistory ".(?<passedURL>http(|s)://..(net|com|org|io)).*" | stats dc(event_simpleName) as eventCount, values(ComputerName) as ComputerName, values(FileName) as FileName, values(UserSid_readable) as UserSid_readable, values(CommandHistory) as CommandHistory, values(passedURL) as passed …
