---
title: "Parsing Linux Kernel Version"
date: 2021-10-08
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/q3xscp/20211008_cool_query_friday_parsing_linux_kernel/"
mitre: []
series: Cool Query Friday
---

# Parsing Linux Kernel Version

> Source: [https://www.reddit.com/r/crowdstrike/comments/q3xscp/20211008_cool_query_friday_parsing_linux_kernel/](https://www.reddit.com/r/crowdstrike/comments/q3xscp/20211008_cool_query_friday_parsing_linux_kernel/) — by Andrew-CS (CrowdStrike) — 2021-10-08

Welcome to our twenty-sixth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
|  rex field=OSVersionString "Linux\s+\S+\s+(?<kernelVersion>.*)\s+\#.*"
```

## Query 2
```cql
event_platform=lin event_simpleName=OsVersionInfo
|  rex field=OSVersionString "Linux\s+\S+\s+(?<kernelVersion>.*)\s+\#.*"
| fields aid, ComputerName, AgentVersion, kernelVersion
```

## Query 3
```cql
| stats latest(kernelVersion) as kernelVersion by aid
```

## Query 4
```cql
index=main sourcetype=OsVersionInfo* event_platform=lin event_simpleName=OsVersionInfo
| fields aid, OSVersionString
| rex field=OSVersionString "Linux\s+\S+\s+(?<kernelVersion>.*)\s+\#.*"
| stats latest(kernelVersion) as kernelVersion by aid
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Timezone, AgentVersion, BiosManufacturer, Continent, Country, FirstSeen
```

## Query 5
```cql
index=main sourcetype=OsVersionInfo* event_platform=lin event_simpleName=OsVersionInfo
| fields aid, OSVersionString
|  rex field=OSVersionString "Linux\s+\S+\s+(?<kernelVersion>.*)\s+\#.*"
| stats latest(kernelVersion) as kernelVersion by aid
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Timezone, AgentVersion, BiosManufacturer, Continent, Country, FirstSeen
| convert ctime(FirstSeen)
| table aid, ComputerName, Version, kernelVersion, AgentVersion, FirstSeen, BiosManufacturer, Continent, Country, Timezone
| rename aid as "Falcon Agent ID", ComputerName as "Endpoint", Version as "OS", kernelVersion as "Kernel", AgentVersion as "Falcon Version", FirstSeen as "Falcon Install Date", BiosManufacturer as "BIOS Maker"
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> Ah! Sorry, I misunderstood. In your RTR feed, do you have the field OSVersionFileData? If yes, what are you using to look at RTR? Splunk?
— [CS] Andrew-CS · score 1
