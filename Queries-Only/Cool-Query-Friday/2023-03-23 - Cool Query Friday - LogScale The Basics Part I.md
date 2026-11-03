---
title: "LogScale: The Basics Part I"
date: 2023-03-23
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/11zojds/20230323_cool_query_friday_logscale_the_basics/"
mitre: []
series: Cool Query Friday
---

# LogScale: The Basics Part I

> Source: [https://www.reddit.com/r/crowdstrike/comments/11zojds/20230323_cool_query_friday_logscale_the_basics/](https://www.reddit.com/r/crowdstrike/comments/11zojds/20230323_cool_query_friday_logscale_the_basics/) — by Andrew-CS (CrowdStrike) — 2023-03-23

Welcome to our fifty-sixth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get all ProcessRollup2 events
#event_simpleName=ProcessRollup2
// Search for system User SID
| UserSid="S-1-5-18"
// Count total executions
| count(aid, as=totalExecutions)
```

## Query 2
```cql
// Account for microseconds or remove decimal point in timestamp
| myTimeStamp := myTimeStamp * 1000
```

## Query 3
```cql
#event_simpleName=ProcessRollup2
// Convert ProcessStartTime to proper epoch format
| ProcessStartTime := ProcessStartTime * 1000
// Convert epoch Time to Human Time
| HumanTime := formatTime("%Y-%m-%d %H:%M:%S.%L", field=ProcessStartTime, locale=en_US, timezone=Z)
| select([ProcessStartTime, HumanTime, aid, ImageFileName])
```

## Query 4
```cql
| timeDelta := now() - (ProcessStartTime*1000)
```

## Query 5
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(System32|SysWow64)\\/i
```

## Query 6
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<systemFolder>(System32|SysWow64))\\/i
| groupBy([systemFolder, ImageFileName])
```

## Query 7
```cql
| case {
UserIsAdmin=1 | UserIsAdmin := "True" ;
UserIsAdmin=0 | UserIsAdmin := "False" ;
* }
```

## Query 8
```cql
| case {
UserIsAdmin=1 | UserIsAdmin_Readable := "True" ;
UserIsAdmin=0 | UserIsAdmin_Readable := "False" ;
* }
```

## Query 9
```cql
#event_simpleName=UserLogon
| $UserIsAdmin()
| select([aid, UserName, UserSid, UserIsAdmin, UserIsAdmin_Readable])
```

## Query 10
```cql
// Get all user logon events for User SID S-1-5-21-*
#event_simpleName=UserLogon event_platform=Win UserSid="S-1-5-21-*"
// Invoke saved query to enrich UserIsAdmin field
| $ConvertUserIsAdmin()
// Use select to output in tabular format
| select([@timestamp, aid, ClientComputerName, UserName, LogonType, UserIsAdmin_Readable])
```

## Query 11
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\powershell\.exe/i
| groupBy(SHA256HashData, function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalExecutions), collect(CommandLine)]))
```

## Query 12
```cql
| groupBy(SHA256HashData, function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalExecutions), collect(CommandLine)]))
```

## Query 13
```cql
| groupBy([SHA256HashData, FileName], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalExecutions), collect(CommandLine)]))
```

## Query 14
```cql
| groupBy([SHA256HashData, FileName], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalExecutions), collect([CommandLine, UserSid])]))
```

## Query 15
```cql
// Get all DNS Request events
#event_simpleName=DnsRequest
// Use regex to determine top level domain
| DomainName=/\.?(?<topLevelDomain>\w+\.\w+$)/i
// Create search box for top level domain
| topLevelDomain=?topLevelDomain
// Count number of domain variations by top level domain
| groupBy(topLevelDomain, function=(count(DomainName, distinct=true, as=domainVariations)))
```

## Query 16
```cql
#event_simpleName=OsVersionInfo
| groupBy("ProductName")
```

## Query 17
```cql
EventType = "Event_ExternalApiEvent" ExternalApiType = "Event_DetectionSummaryEvent"
| sankey(source="Tactic",target="Technique", weight=count(AgentIdString))
```

## Query 18
```cql
EventType="Event_ExternalApiEvent" ExternalApiType="Event_DetectionSummaryEvent"
| groupBy(Severity)
```

## Query 19
```cql
#event_simpleName=UserLogon event_platform=Lin
| UserIsAdmin match {
    1 => UserIsAdmin := "True" ;
    0 => UserIsAdmin := "False" ;
}
| select([@timestamp, UserName, UID, LogonType, UserIsAdmin])
```

## Query 20
```cql
| targetField match {
    value1 => targetField := "substitution1" ;
    value2 => targetField := "substitution2" ;
}
```

## Query 21
```cql
// Get InstalledApplication events for Google Chrome
#event_simpleName=InstalledApplication AppName="Google Chrome"
// Get latest AppVersion for each system
| groupBy(aid, function=([selectLast([AppVendor, AppName, AppVersion, InstallDate])]))
// Use regex to break AppVersion field into components
| AppVersion = /(?<majorVersion>\d+)\.(?<minorVersion>\d+)\.(?<buildNumber>\d+)\.(?<subBuildNumber>\d+)$/i
// Evaluate builds that need to be patched
| case {
    majorVersion>=110 | needsPatch := "No" ;
    majorVersion>=109 AND buildNumber >= 5414 | needsPatch := "No" ;
    majorVersion<=109 AND buildNumber < 5414 | needsPatch := "Yes" ;
    majorVersion<=108 | needsPatch := "Yes" ;
* }
// Check for needed update  and Organize Output
| needsPatch = "Yes"
| select([aid, InstallDate, needsPatch, AppVendor, AppName, AppVersion, InstallDate])
// Convert timestamp
| InstallDate := InstallDate *1000
| InstallDate := formatTime("%Y-%m-%d", field=InstallDate, locale=en_US, timezone=Z)
```

## Query 22
```cql
#event_simpleName=ProcessRollup2 ImageFileName=/\\(?<fileName>\w+\.\w+$)/i
| regex("(?<fourLetterFileName>^\w{4})\.exe", field=fileName, strict=false)
| groupBy([fileName, fourLetterFileName])
```

## Query 23
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-e(nc|ncodedcommand|ncoded)?\s+/i
```

## Query 24
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-(?<encodedFlagUsed>e(nc|ncodedcommand|ncoded)?)\s+/i
```

## Query 25
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-(?<encodedFlagUsed>e(nc|ncodedcommand|ncoded)?)\s+/i
| UserSid="S-1-5-18"
```

## Query 26
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-(?<encodedFlagUsed>e(nc|ncodedcommand|ncoded)?)\s+/i
| UserSid="S-1-5-18"
| groupBy([encodedFlagUsed, CommandLine], function=(count(aid, as=executionCount)))
| sort(executionCount, order=asc)
```

## Query 27
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-(?<encodedFlagUsed>e(nc|ncodedcommand|ncoded)?)\s+/i
// | UserSid="S-1-5-18"
| groupBy([encodedFlagUsed, CommandLine], function=(count(aid, as=executionCount)))
| sort(executionCount, order=asc)
```

## Query 28
```cql
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/\\powershell(_ise)?\.exe/i
| CommandLine=/\-(?<encodedFlagUsed>e(nc|ncodedcommand|ncoded)?)\s+/i
//| UserSid="S-1-5-18"
| groupBy([encodedFlagUsed, CommandLine], function=(count(aid, as=executionCount)))
| test(executionCount < 10)
| sort(executionCount, order=asc)
```

## Query 29
```cql
| format("%,.100s", field=CommandLine, as=CommandLine)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| match(file="lookup-file.csv", column=aid, field=aid, include=[Version, AgentVersion])
```
— [CS] Andrew-CS · comment score 2

### Q&A

**Q — [Community] mattdufrene:** in LogScale, is it possible to reference multiple fields/columns in a lookup table?

**A — [CS] Andrew-CS:** Like all languages, you need a single key field to specify a "row" but you can output multiple "columns" related to that key field. Example: | match(file="lookup-file.csv", column=aid, field=aid, include=[Version, AgentVersion]) Documentation is [here](https://library.humio.com/falcon-logscale/functions-match.html#functions-match-examples).

**Q — [Community] mattdufrene:** We're currently a Splunk shop, but recently pulled the trigger to migrate to LogScale. We are in the process of migrating searches and are working out the best way to leverage our lookup tables. In Splunk, you could match against values from multiple columns. For example: `| search [ inputlookup loo …

**A — [CS] Andrew-CS:** Hey! Thanks for choosing LogScale! I don't know the exact answer to this question, so I'm going to tag in u/AHogan-CS to see if he knows.

**Q — [Community] BigOwlCriesForLogs:** LogScale looks like an amazing product. Is there a way to try it out and play with it on my own?

**A — [CS] Andrew-CS:** >If you want to mess around with LogScale on your own, there is a free Community Edition available. If you want to mess around with LogScale on your own, there is a [free Community Edition available](http://cloud.community.humio.com/).
