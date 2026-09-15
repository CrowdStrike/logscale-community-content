---
title: "Electric Slide… ‘ing Time Windows"
date: 2025-02-28
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1izst3r/20250228_cool_query_friday_electric_slide_ing/"
mitre: []
series: Cool Query Friday
---

# Electric Slide… ‘ing Time Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/1izst3r/20250228_cool_query_friday_electric_slide_ing/](https://www.reddit.com/r/crowdstrike/comments/1izst3r/20250228_cool_query_friday_electric_slide_ing/) — by Andrew-CS (CrowdStrike) — 2025-02-28

Welcome to our eighty-third installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get all Windows Process Execution Events
#event_simpleName=ProcessRollup2 event_platform=Win

// Restrict by common files used in Discovery TA0007
| in(field="FileName", values=[ping.exe, net.exe, tracert.exe, whoami.exe, ipconfig.exe, nltest.exe, reg.exe, systeminfo.exe, hostname.exe], ignoreCase=true)
```

## Query 2
```cql
// Aggregate by key fields Agent ID and timestamp to arrange in sequence; collect relevant fields for use later
| groupBy([aid, u/timestamp], function=([collect([#event_simpleName, ComputerName, UserName, UserSid, FileName], multival=false)]), limit=max)
```

## Query 3
```cql
// Use slidingTimeWindow to look for 4 or more Discovery commands in a 10 minute window
| groupBy(
   aid,
   function=slidingTimeWindow(
       [{#event_simpleName=ProcessRollup2 | count(FileName, as=DiscoveryCount, distinct=true)}, {collect([FileName])}],
       span=10m
   ), limit=max
 )
```

## Query 4
```cql
// This is the Discovery command threshold
| DiscoveryCount >= 4
```

## Query 5
```cql
// Get all Windows Process Execution Events
#event_simpleName=ProcessRollup2 event_platform=Win

// Restrict by common files used in Discovery TA0007
| in(field="FileName", values=[ping.exe, net.exe, tracert.exe, whoami.exe, ipconfig.exe, nltest.exe, reg.exe, systeminfo.exe, hostname.exe], ignoreCase=true)

// Aggregate by key fields Agent ID and timestamp to arrange in sequence; collect relevant fields for use later
| groupBy([aid, @timestamp], function=([collect([#event_simpleName, ComputerName, UserName, UserSid, FileName], multival=false)]), limit=max)

// Use slidingTimeWindow to look for 4 or more Discovery commands in a 10 minute window
| groupBy(
   aid,
   function=slidingTimeWindow(
       [{#event_simpleName=ProcessRollup2 | count(FileName, as=DiscoveryCount, distinct=true)}, {collect([FileName])}],
       span=10m
   ), limit=max
 )
// This is the Discovery command threshold
| DiscoveryCount >= 4
| drop([#event_simpleName])
```

## Query 6
```cql
// Get successful and failed user logon events
(#event_simpleName=UserLogon OR #event_simpleName=UserLogonFailed2) UserName!=/^(DWM|UMFD)-\d+$/

// Restrict to LogonType 2 and 10 (interactive)
| in(field="LogonType", values=[2, 10])

// Aggregate by key fields Agent ID and timestamp; collect the fields of interest
| groupBy([aid, @timestamp], function=([collect([event_platform, #event_simpleName, UserName], multival=false), selectLast([ComputerName])]), limit=max)
```

## Query 7
```cql
// Use slidingTimeWindow to look for 3 or more failed user login events on a single Agent ID followed by a successful login event in a 10 minute window
| groupBy(
   aid,
   function=slidingTimeWindow(
       [{#event_simpleName=UserLogonFailed2 | count(as=FailedLogonAttempts)}, {collect([UserName]) | rename(field="UserName", as="FailedLogonAccounts")}],
       span=10m
   ), limit=max
 )

// Rename fields
| rename([[UserName,LastSuccessfulLogon],[@timestamp,LastLogonTime]])

// This is the FailedLogonAttempts threshold
| FailedLogonAttempts >= 3

// This is the event that needs to occur after the threshold is met
| #event_simpleName=UserLogon
```

## Query 8
```cql
// Convert LastLogonTime to Human Readable format
| LastLogonTime:=formatTime(format="%F %T.%L %Z", field="LastLogonTime")

// User Search; uncomment out one cloud
| rootURL  := "https://falcon.crowdstrike.com/"
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/"
//rootURL  := "https://falcon.eu-1.crowdstrike.com/"
//rootURL  := "https://falcon.us-2.crowdstrike.com/"
| format("[Scope User](%sinvestigate/dashboards/user-search?isLive=false&sharedTime=true&start=7d&user=%s)", field=["rootURL", "LastSuccessfulLogon"], as="User Search")

// Asset Graph
| format("[Scope Asset](%sasset-details/managed/%s)", field=["rootURL", "aid"], as="Asset Graph")

// Adding description
| Description:=format(format="User %s logged on to system %s (Agent ID: %s) successfully after %s failed logon attempts were observed on the host.", field=[LastSuccessfulLogon, ComputerName, aid, FailedLogonAttempts])

// Final field organization
| groupBy([aid, ComputerName, event_platform, LastSuccessfulLogon, LastLogonTime, FailedLogonAccounts, FailedLogonAttempts, "User Search", "Asset Graph", Description], function=[], limit=max)
```

## Query 9
```cql
// Get successful and failed user logon events
(#event_simpleName=UserLogon OR #event_simpleName=UserLogonFailed2) UserName!=/^(DWM|UMFD)-\d+$/

// Restrict to LogonType 2 and 10
| in(field="LogonType", values=[2, 10])

// Aggregate by key fields Agent ID and timestamp; collect the event name
| groupBy([aid, @timestamp], function=([collect([event_platform, #event_simpleName, UserName], multival=false), selectLast([ComputerName])]), limit=max)

// Use slidingTimeWindow to look for 3 or more failed user login events on a single Agent ID followed by a successful login event in a 10 minute window
| groupBy(
   aid,
   function=slidingTimeWindow(
       [{#event_simpleName=UserLogonFailed2 | count(as=FailedLogonAttempts)}, {collect([UserName]) | rename(field="UserName", as="FailedLogonAccounts")}],
       span=10m
   ), limit=max
 )

// Rename fields
| rename([[UserName,LastSuccessfulLogon],[@timestamp,LastLogonTime]])

// This is the FailedLogonAttempts threshold
| FailedLogonAttempts >= 3

// This is the event that needs to occur after the threshold is met
| #event_simpleName=UserLogon

// Convert LastLogonTime to Human Readable format
| LastLogonTime:=formatTime(format="%F %T.%L %Z", field="LastLogonTime")

// User Search; uncomment out one cloud
| rootURL  := "https://falcon.crowdstrike.com/"
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/"
//rootURL  := "https://falcon.eu-1.crowdstrike.com/"
//rootURL  := "https://falcon.us-2.crowdstrike.com/"
| format("[Scope User](%sinvestigate/dashboards/user-search?isLive=false&sharedTime=true&start=7d&user=%s)", field=["rootURL", "LastSuccessfulLogon"], as="User Search")

// Asset Graph
| format("[Scope Asset](%sasset-details/managed/%s)", field=["rootURL", "aid"], as="Asset Graph")

// Adding description
| Description:=format(format="User %s logged on to system %s (Agent ID: %s) successfully after %s failed logon attempts were observed on the host.", field=[LastSuccessfulLogon, ComputerName, aid, FailedLogonAttempts])

// Final field organization
| groupBy([aid, ComputerName, event_platform, LastSuccessfulLogon, LastLogonTime, FailedLogonAccounts, FailedLogonAttempts, "User Search", "Asset Graph", Description], function=[], limit=max)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| createEvents(["name=andrew-cs, shirt_color=blue", "name=andrew-cs, shirt_color=red", "name=andrew-cs, shirt_color=green"])
| kvParse()
| groupBy([name], function=([collect([shirt_color])]))

| createEvents(["name=andrew-cs, shirt_color=blue", "name=andrew-cs, shirt_color=red", "name=andrew-cs, shirt_color=green"])
| kvParse()
| groupBy([name], function=([collect([shirt_color], multival=false)]))
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] sixstringacks:** I’m trying the understand the multival parameter of collect a little better and the documentation is not clear. Can you explain the purpose of setting multival to false? Reviewing the results of the first groupBy query, setting multival=false or multival=true does not seem to affect the results.

**A — [CS] Andrew-CS:** In the query above, it's to account for an edge case where two users with distinct user names attempt to login at the EXACT same time (down to the millisecond). I don't even know if that's possible, but that's why it's there. To see what multival does, run these two queries... | createEvents(["name=andrew-cs, shirt_color=blue", "name=andrew-cs, shirt_color=red", "name=andrew-cs, shirt_color=green"]) | kvParse() | groupBy([name], function=([collect([shirt_color])])) | createEvents(["name=andrew-c …
