---
title: "Hunting for Typosquatted Domains"
date: 2026-03-02
author: "Dylan-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1rixd9d/20260302_cool_query_friday_hunting_for/"
mitre: []
series: Cool Query Friday
---

# Hunting for Typosquatted Domains

> Source: [https://www.reddit.com/r/crowdstrike/comments/1rixd9d/20260302_cool_query_friday_hunting_for/](https://www.reddit.com/r/crowdstrike/comments/1rixd9d/20260302_cool_query_friday_hunting_for/) — by Dylan-CS (CrowdStrike) — 2026-03-02

Welcome back to another installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22) (on a Monday). I’ll be your guest host for today’s session. As always, the format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Normalize input as a URI so we can reliably work with hostnames
| parseUri(DomainName, defaultBase="https://")

// Extract the registrable/base domain into base_domain (extend TLD list as needed)
| DomainName.host=/(?<base_domain>[-a-zA-Z0-9]+\.(?:co\.uk|com\.tr|com|net|org|edu|gov|io|co))$/
```

## Query 2
```cql
// Compare the observed base_domain against the provided reference domain
| text:editDistance(
    target=base_domain,
    reference="crowdstrike.com",
    maxDistance=10,
    ignoreCase=true,
    as=lev_dist)
```

## Query 3
```cql
// Remove exact matches (distance 0 means it is one of our legitimate reference domains)
| lev_dist != 0

// Keep only near matches for triage (tune as needed)
| lev_dist <=3
```

## Query 4
```cql
// Get DNS request telemetry from Falcon sensor
#event_simpleName=DnsRequest

// Normalize input as a URI so we can reliably work with hostnames
| parseUri(DomainName, defaultBase="https://")

// Extract the registrable/base domain into base_domain (extend TLD list as needed)
| DomainName.host=/(?<base_domain>[-a-zA-Z0-9]+\.(?:co\.uk|com\.tr|com|net|org|edu|gov|io|co))$/

// Compare the observed base_domain against the provided reference domain
| text:editDistance(
    target=base_domain,
    reference="crowdstrike.com",
    maxDistance=10,
    ignoreCase=true,
    as=lev_dist)

// Remove exact matches (distance 0 means it is one of our legitimate reference domains)
| lev_dist != 0

// Keep only near matches for triage (tune as needed)
| lev_dist <=3
```

## Query 5
```cql
// Compare the observed base_domain to multiple reference domains
| text:editDistanceAsArray(
    target=base_domain,
    references=["crowdstrike.com","servicenowservices.com"],
    maxDistance=10
)
```

## Query 6
```cql
// Split the _distance[] object array so each reference comparison becomes its own row
| split(_distance)

// Remove exact matches (distance 0 means it is one of our legitimate reference domains)
| _distance.distance != 0

// Keep only near matches for triage (tune as needed)
| _distance.distance <= 3
```

## Query 7
```cql
// Rename fields for clarity in the output
| Reference_Domain:=_distance.reference
| Observed_Domain:=base_domain
| lev_dist:=_distance.distance

// Output results and sort by closest match first
| groupBy([Observed_Domain,Reference_Domain,lev_dist], function=collect([DomainName,ComputerName,aid]), limit=max)
| sort(lev_dist, order=asc)

// Intelligence Graph; uncomment out one cloud
| rootURL := "https://falcon.crowdstrike.com/"
// | rootURL := "https://falcon.laggar.gcw.crowdstrike.com/"
// | rootURL := "https://falcon.eu-1.crowdstrike.com/"
// | rootURL := "https://falcon.us-2.crowdstrike.com/"
| format("[Link](%sinvestigate/dashboards/domain-search?isLive=false&sharedTime=true&start=7d&domain=*%s)", field=["rootURL", "Observed_Domain"], as="Domain Search")

| drop(rootURL)
```

## Query 8
```cql
// Get DNS request telemetry from Falcon sensor
#event_simpleName=DnsRequest

// Normalize input as a URI so we can reliably work with hostnames
| parseUri(DomainName, defaultBase="https://")

// Extract the registrable/base domain into base_domain (extend TLD list as needed)
| DomainName.host=/(?<base_domain>[-a-zA-Z0-9]+\.(?:co\.uk|com\.tr|com|net|org|edu|gov|io|co))$/

// Compare the observed base_domain to multiple reference domains
| text:editDistanceAsArray(
    target=base_domain,
    references=["crowdstrike.com","servicenowservices.com"],
    maxDistance=10
)

// Split the _distance[] object array so each reference comparison becomes its own row
| split(_distance)

// Remove exact matches (distance 0 means it is one of our legitimate reference domains)
| _distance.distance != 0

// Keep only near matches for triage (tune as needed)
| _distance.distance <= 3

// Rename fields for clarity in the output
| Reference_Domain:=_distance.reference
| Observed_Domain:=base_domain
| lev_dist:=_distance.distance

// Output results and sort by closest match first
| groupBy([Observed_Domain,Reference_Domain,lev_dist], function=collect([DomainName,ComputerName,aid]), limit=max)
| sort(lev_dist, order=asc)

// Intelligence Graph; uncomment out one cloud
| rootURL := "https://falcon.crowdstrike.com/"
// | rootURL := "https://falcon.laggar.gcw.crowdstrike.com/"
// | rootURL := "https://falcon.eu-1.crowdstrike.com/"
// | rootURL := "https://falcon.us-2.crowdstrike.com/"
| format("[Link](%sinvestigate/dashboards/domain-search?isLive=false&sharedTime=true&start=7d&domain=*%s)", field=["rootURL", "Observed_Domain"], as="Domain Search")

| drop(rootURL)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
// Technique: T1036.005 - Masquerading: Match Legitimate Name or Location
#event_simpleName=ProcessRollup2

// Extract just the filename from the full path
| ImageFileName=/(?<process_name>[^\\\/]+)$/

// Calculate Levenshtein distance against the legitimate process name
| text:editDistance(
    target=process_name,
    reference="svchost.exe",
    maxDistance=5,
    ignoreCase=true,
    as=name_distance)

// Exclude exact matches — we want near-misses only
| name_distance > 0

// Keep only close lookalikes (1-2 edits = high confidence masquerading)
| name_distance <= 2

// Exclude known legitimate Windows binaries that fall within edit distance
| !in(process_name, values=[
    "sihost.exe",
    "conhost.exe",
    "dllhost.exe",
    "taskhost.exe",
    "wshost.exe",
    "srmhost.exe",
    "SMSvcHost.exe"
  ])

// Sort by closest match for triage priority
| groupBy([process_name, name_distance], function=[count(as=execution_count), collect([ComputerName, ImageFileName, CommandLine, ParentBaseFileName, UserName, SHA256HashData])], limit=10000)
| sort(name_distance, order=asc)
```
— [Community] strawhatintel · comment score 2

```cql
| groupBy([Observed_Domain,Reference_Domain,lev_dist], function=[selectLast(@timestamp),collect([DomainName,ComputerName,aid])], limit=max)
```
— [CS] Dylan-CS · comment score 5

### Q&A

**Q — [Community] Charming_Antelope452:** Is it possible to swap out the domains array (references=\["crowdstrike.com","servicenowservices.com"\]) for references=\[match(domainslist.csv ...)? This would help clean up the rule when looking for many domains, i tried to get it work but it wouldnt produce any results Thanks

**A — [CS] Dylan-CS:** Hi! As of now, there's not a great way to accomplish that. I've passed along your feedback to the team.
