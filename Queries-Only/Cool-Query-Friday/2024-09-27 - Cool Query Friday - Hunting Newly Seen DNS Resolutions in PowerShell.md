---
title: "Hunting Newly Seen DNS Resolutions in PowerShell"
date: 2024-09-27
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1fqokic/20240927_cool_query_friday_hunting_newly_seen_dns/"
mitre: []
series: Cool Query Friday
---

# Hunting Newly Seen DNS Resolutions in PowerShell

> Source: [https://www.reddit.com/r/crowdstrike/comments/1fqokic/20240927_cool_query_friday_hunting_newly_seen_dns/](https://www.reddit.com/r/crowdstrike/comments/1fqokic/20240927_cool_query_friday_hunting_newly_seen_dns/) — by Andrew-CS (CrowdStrike) — 2024-09-27

Welcome to our seventy-eighth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Use case() to create buckets; "Current" will be within last one day and "Historical" will be anything before the past 1d as defined by the time-picker
| case {
    test(@timestamp < (now() - duration(1d))) | HistoricalState:="1";
    test(@timestamp > (now() - duration(1d))) | CurrentState:="1";
}
// Set default values for HistoricalState and CurrentState
| default(value="0", field=[HistoricalState, CurrentState])
```

## Query 2
```cql
// Aggregate by Historical or Current status and DomainName; gather helpful metrics
| groupBy([DomainName], function=[max("HistoricalState",as=HistoricalState), max(CurrentState, as=CurrentState), max(ContextTimeStamp, as=LastSeen), count(aid, as=ResolutionCount), count(aid, distinct=true, as=EndpointCount), collect([FirstIP4Record])], limit=max)

// Check to make sure that the DomainName field as NOT been seen in the Historical dataset and HAS been seen in the current dataset
| HistoricalState=0 AND CurrentState=1
```

## Query 3
```cql
// Get DnsRequest events tied to PowerShell
#event_simpleName=DnsRequest event_platform=Win ContextBaseFileName=powershell.exe

// Use case() to create buckets; "Current" will be withing last one day and "Historical" will be anything before the past 1d as defined by the time-picker
| case {
    test(@timestamp < (now() - duration(1d))) | HistoricalState:="1";
    test(@timestamp > (now() - duration(1d))) | CurrentState:="1";
}

// Set default values for HistoricalState and CurrentState
| default(value="0", field=[HistoricalState, CurrentState])

// Aggregate by Historical or Current status and DomainName; gather helpful metrics
| groupBy([DomainName], function=[max("HistoricalState",as=HistoricalState), max(CurrentState, as=CurrentState), max(ContextTimeStamp, as=LastSeen), count(aid, as=ResolutionCount), count(aid, distinct=true, as=EndpointCount), collect([FirstIP4Record])], limit=max)

// Check to make sure that the DomainName field as NOT been seen in the Historical dataset and HAS been seen in the current dataset
| HistoricalState=0 AND CurrentState=1
```

## Query 4
```cql
// Convert LastSeen to Human Readable
| LastSeen:=formatTime(format="%F %T %Z", field="LastSeen")
```

## Query 5
```cql
// Get GeoIP data for first IPv4 record of domain name
| ipLocation(FirstIP4Record)
```

## Query 6
```cql
// SET FLACON CLOUD; ADJUST COMMENTS TO YOUR CLOUD
| rootURL := "https://falcon.crowdstrike.com/" /* US-1*/
//rootURL  := "https://falcon.eu-1.crowdstrike.com/" ; /*EU-1 */
//rootURL  := "https://falcon.us-2.crowdstrike.com/" ; /*US-2 */
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" ; /*GOV-1 */

// Create link to Indicator Graph for easier scoping
| format("[Indicator Graph](%sintelligence/graph?indicators=domain:'%s')", field=["rootURL", "DomainName"], as="Indicator Graph")

// Create link to Domain Search for easier scoping
| format("[Domain Search](%sinvestigate/dashboards/domain-search?domain=%s&isLive=false&sharedTime=true&start=7d)", field=["rootURL", "DomainName"], as="Search Domain")
```

## Query 7
```cql
// Drop HistoricalState, CurrentState, Latitude, Longitude, and rootURL (optional)
| drop([HistoricalState, CurrentState, FirstIP4Record.lat, FirstIP4Record.lon, rootURL])

// Set default values for GeoIP fields to make output look prettier (optional)
| default(value="-", field=[FirstIP4Record.country, FirstIP4Record.city, FirstIP4Record.state])
```

## Query 8
```cql
// Get DnsRequest events tied to PowerShell
#event_simpleName=DnsRequest event_platform=Win ContextBaseFileName=powershell.exe

// Use case() to create buckets; "Current" will be withing last one day and "Historical" will be anything before the past 1d as defined by the time-picker
| case {
    test(@timestamp < (now() - duration(1d))) | HistoricalState:="1";
    test(@timestamp > (now() - duration(1d))) | CurrentState:="1";
}

// Set default values for HistoricalState and CurrentState
| default(value="0", field=[HistoricalState, CurrentState])

// Aggregate by Historical or Current status and DomainName; gather helpful metrics
| groupBy([DomainName], function=[max("HistoricalState",as=HistoricalState), max(CurrentState, as=CurrentState), max(ContextTimeStamp, as=LastSeen), count(aid, as=ResolutionCount), count(aid, distinct=true, as=EndpointCount), collect([FirstIP4Record])], limit=max)

// Check to make sure that the DomainName field as NOT been seen in the Historical dataset and HAS been seen in the current dataset
| HistoricalState=0 AND CurrentState=1

// Convert LastSeen to Human Readable
| LastSeen:=formatTime(format="%F %T %Z", field="LastSeen")

// Get GeoIP data for first IPv4 record of domain name
| ipLocation(FirstIP4Record)

// SET FLACON CLOUD; ADJUST COMMENTS TO YOUR CLOUD
| rootURL := "https://falcon.crowdstrike.com/" /* US-1*/
//rootURL  := "https://falcon.eu-1.crowdstrike.com/" ; /*EU-1 */
//rootURL  := "https://falcon.us-2.crowdstrike.com/" ; /*US-2 */
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" ; /*GOV-1 */

// Create link to Indicator Graph for easier scoping
| format("[Indicator Graph](%sintelligence/graph?indicators=domain:'%s')", field=["rootURL", "DomainName"], as="Indicator Graph")

// Create link to Domain Search for easier scoping
| format("[Domain Search](%sinvestigate/dashboards/domain-search?domain=%s&isLive=false&sharedTime=true&start=7d)", field=["rootURL", "DomainName"], as="Search Domain")

// Drop HistoricalState, CurrentState, Latitude, Longitude, and rootURL (optional)
| drop([HistoricalState, CurrentState, FirstIP4Record.lat, FirstIP4Record.lon, rootURL])

// Set default values for GeoIP fields to make output look prettier
| default(value="-", field=[FirstIP4Record.country, FirstIP4Record.city, FirstIP4Record.state])
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
// Get DnsRequest events tied to PowerShell
#event_simpleName=DnsRequest event_platform=Win ContextBaseFileName=powershell.exe
| DomainName!=/(.?myinternaldomain.com$)/
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] yankeesfan01x:** Is there a way to only include external DNS name resolutions and nothing internal?

**A — [CS] Andrew-CS:** How do you classify internal? You could make the first two lines something like: // Get DnsRequest events tied to PowerShell #event_simpleName=DnsRequest event_platform=Win ContextBaseFileName=powershell.exe | DomainName!=/(.?myinternaldomain.com$)/
