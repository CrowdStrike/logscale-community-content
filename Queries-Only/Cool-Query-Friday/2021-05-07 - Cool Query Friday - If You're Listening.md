---
title: "If You're Listening"
date: 2021-05-07
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/n6xwv6/20210507_cool_query_friday_if_youre_listening/"
mitre: []
series: Cool Query Friday
---

# If You're Listening

> Source: [https://www.reddit.com/r/crowdstrike/comments/n6xwv6/20210507_cool_query_friday_if_youre_listening/](https://www.reddit.com/r/crowdstrike/comments/n6xwv6/20210507_cool_query_friday_if_youre_listening/) — by Andrew-CS (CrowdStrike) — 2021-05-07

Welcome to our tenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_simpleName=NetworkListenIP4 OR event_simpleName=NetworkListenIP6
| stats dc(aid) as endpointCount dc(LPort) as listeningPorts by event_simpleName
```

## Query 2
```cql
event_platform=win event_simpleName=NetworkListenIP4 
| fields aid, aip, LocalAddressIP4, ComputerName, Protocol_decimal, LPort
```

## Query 3
```cql
event_platform=win event_simpleName=NetworkListenIP4 
| fields aid, aip, LocalAddressIP4, ComputerName, Protocol_decimal, LPort 
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
```

## Query 4
```cql
event_platform=win event_simpleName=NetworkListenIP4 
| fields aid, aip, LocalAddressIP4, ComputerName, Protocol_decimal, LPort 
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
| stats dc(LPort) as openPortCount values(LPort) as openPorts by aid, ComputerName, SystemType, Version, Protocol, aip, LocalAddressIP4
| sort -openPortCount, +ComputerName
```

## Query 5
```cql
event_platform=win event_simpleName=NetworkListenIP4 
| fields aid, aip, LocalAddressIP4, ComputerName, Protocol_decimal, LPort 
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
| stats values(Protocol) as listeningProtocols dc(aid) as systemCount values(Version) as osVersions by SystemType, LPort
| rename LPort as listeningPort, SystemType as systemType
| sort - systemCount
```

## Query 6
```cql
event_platform=win event_simpleName=NetworkListenIP4 LPort<10000
| fields aid, aip, LocalAddressIP4, ComputerName, Protocol_decimal, LPort 
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
| stats values(Protocol) as listeningProtocols dc(aid) as systemCount values(Version) as osVersions by SystemType, LPort
| rename LPort as listeningPort, SystemType as systemType
| sort - systemCount
```

## Query 7
```cql
| eval falconPID=mvappend(TargetProcessId_decimal, ContextProcessId_decimal)
```

## Query 8
```cql
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
```

## Query 9
```cql
| stats dc(event_simpleName) as events values(SystemType) as systemType values(Version) as osVersion latest(aip) as externalIP latest(LocalAddressIP4) as internalIP values(FileName) as listeningFile values(UserName) as userName values(UserSid_readable) as userSID values(LPort) as listeningPort values(Protocol) as listeningProtocol by aid, ComputerName, falconPID
| where events > 1
```

## Query 10
```cql
(event_platform=win AND event_simpleName=NetworkListenIP4 AND LPort>10000) OR (event_platform=win AND event_simpleName=ProcessRollup2) 
| eval falconPID=mvappend(TargetProcessId_decimal, ContextProcessId_decimal)
| lookup aid_master aid OUTPUT ProductType Version
| eval Protocol=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| eval SystemType=case(ProductType=1, "Workstation", ProductType=2, "Domain Controller", ProductType=3, "Server")
| stats dc(event_simpleName) as events latest(SystemType) as systemType latest(Version) as osVersion latest(aip) as externalIP latest(LocalAddressIP4) as internalIP values(FileName) as listeningFile values(UserName) as userName values(UserSid_readable) as userSID values(LPort) as listeningPort values(Protocol) as listeningProtocol by aid, ComputerName, falconPID
| where events > 1
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> Hi there. You have to enable network events for Linux. It's in the Linux prevention policy: [https://imgur.com/a/sW4MqW1](https://imgur.com/a/sW4MqW1) We provide this option on Linux in the event customers want to disable it on high-performance compute clusters that are calibrated to a very, very precise performance metric.
— [CS] Andrew-CS · score 2
