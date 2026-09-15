---
title: "Hunting Rogue DNS Servers"
date: 2021-06-11
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/nxfcnu/20210611_cool_query_friday_hunting_rogue_dns/"
mitre: []
series: Cool Query Friday
---

# Hunting Rogue DNS Servers

> Source: [https://www.reddit.com/r/crowdstrike/comments/nxfcnu/20210611_cool_query_friday_hunting_rogue_dns/](https://www.reddit.com/r/crowdstrike/comments/nxfcnu/20210611_cool_query_friday_hunting_rogue_dns/) — by Andrew-CS (CrowdStrike) — 2021-06-11

Welcome to our fourteenth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer
```

## Query 2
```cql
[...]
| rex field=DomainName "[@\.](?<tlDomain>\w+\.\w+)$"
```

## Query 3
```cql
[...]
| stats dc(aid) as uniqueEndpoints count(aid) as totalResoultions dc(tlDomain) as domainsResolved by RespondingDnsServer
| sort - totalResoultions
```

## Query 4
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer
| rex field=DomainName "[\.](?<tlDomain>\w+\.\w+)$"
| stats dc(aid) as uniqueEndpoints count(aid) as totalResoultions dc(tlDomain) as domainsResolved by RespondingDnsServer
| sort - totalResoultions
```

## Query 5
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer, LocalAddressIP4
| rex field=DomainName "[\.](?<tlDomain>\w+\.\w+)$"
| top tlDomain limit=50
```

## Query 6
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer, LocalAddressIP4
| rex field=DomainName "[\.](?<tlDomain>\w+\.\w+)$"
| top tlDomain by RespondingDnsServer limit=1
| sort +RespondingDnsServer, -count
```

## Query 7
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer, LocalAddressIP4
| rex field=DomainName "[\.](?<tlDomain>\w+\.\w+)$" 
| top DomainName by tlDomain limit=5
| stats values(DomainName) as domainName by tlDomain
| sort + tlDomain
```

## Query 8
```cql
event_simpleName=DnsRequest 
| where isnotnull(RespondingDnsServer)
| fields aip, aid, cid, company, ComputerName, DomainName, RespondingDnsServer, LocalAddressIP4
| rex field=DomainName "[\.](?<tlDomain>\w+\.\w+)$" 
| stats values(ComputerName) as endpointName count(DomainName) as totalResolutions by aid
| sort - totalResolutions
```
