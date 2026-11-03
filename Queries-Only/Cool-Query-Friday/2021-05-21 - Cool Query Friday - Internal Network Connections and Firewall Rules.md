---
title: "Internal Network Connections and Firewall Rules"
date: 2021-05-21
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/nhs906/20210521_cool_query_friday_internal_network/"
mitre: []
series: Cool Query Friday
---

# Internal Network Connections and Firewall Rules

> Source: [https://www.reddit.com/r/crowdstrike/comments/nhs906/20210521_cool_query_friday_internal_network/](https://www.reddit.com/r/crowdstrike/comments/nhs906/20210521_cool_query_friday_internal_network/) — by Andrew-CS (CrowdStrike) — 2021-05-21

Welcome to our twelfth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_simpleName=NetworkListenIP4
| fields aid, ComputerName, LocalAddressIP4, LocalPort_decimal, ProductType, Protocol_decimal
```

## Query 2
```cql
event_simpleName=NetworkListenIP4 ProductType!=1
| fields aid, ComputerName, LocalAddressIP4, LocalPort_decimal, ProductType, Protocol_decimal
```

## Query 3
```cql
event_simpleName=NetworkListenIP4 ProductType!=1
| lookup local=true aid_master aid OUTPUT Version, MachineDomain, OU, SiteName, Timezone 
| fields aid, ComputerName, LocalAddressIP4, LocalPort_decimal, MachineDomain, OU, ProductType, Protocol_decimal, SiteName, Timezone, Version
```

## Query 4
```cql
event_simpleName=NetworkListenIP4 ProductType!=1 (LocalAddressIP4=172.16.0.0/12 OR LocalAddressIP4=192.168.0.0/16 OR LocalAddressIP4=10.0.0.0/8)
| lookup local=true aid_master aid OUTPUT Version, MachineDomain, OU, SiteName, Timezone 
| fields aid, ComputerName, LocalAddressIP4, LocalPort_decimal, MachineDomain, OU, ProductType, Protocol_decimal, SiteName, Timezone, Version
```

## Query 5
```cql
| lookup local=true aid_master aid OUTPUT Version, MachineDomain, OU, SiteName, Timezone
```

## Query 6
```cql
| eval Protocol_decimal=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| stats values(ComputerName) as hostNames values(LocalAddressIP4) as localIPs values(Version) as osVersion values(MachineDomain) as machineDomain values(OU) as organizationalUnit values(SiteName) as siteName values(Timezone) as timeZone values(LocalPort_decimal) as listeningPorts values(Protocol_decimal) as protocolsUsed by aid
```

## Query 7
```cql
event_simpleName=NetworkListenIP4 ProductType!=1 (LocalAddressIP4=172.16.0.0/12 OR LocalAddressIP4=192.168.0.0/16 OR LocalAddressIP4=10.0.0.0/8)
| lookup local=true aid_master aid OUTPUT Version, MachineDomain, OU, SiteName, Timezone 
| fields aid, ComputerName, LocalAddressIP4, LocalPort_decimal, MachineDomain, OU, ProductType, Protocol_decimal, SiteName, Timezone, Version
| where LocalPort_decimal < 10000
| eval Protocol_decimal=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| stats values(ComputerName) as hostNames values(LocalAddressIP4) as localIPs values(Version) as osVersion values(MachineDomain) as machineDomain values(OU) as organizationalUnit values(SiteName) as siteName values(Timezone) as timeZone values(LocalPort_decimal) as listeningPorts values(Protocol_decimal) as protocolsUsed by aid
```

## Query 8
```cql
event_simpleName=NetworkListenIP4 ProductType!=1 (LocalAddressIP4=172.16.0.0/12 OR LocalAddressIP4=192.168.0.0/16 OR LocalAddressIP4=10.0.0.0/8)
| where LocalPort_decimal < 10000
| eval Protocol_decimal=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| stats dc(aid) as uniqueServers by LocalPort_decimal, Protocol_decimal
| sort - uniqueServers
| rename LocalPort_decimal as listeningPort, Protocol_decimal as Protocol
```

## Query 9
```cql
event_simpleName=NetworkListenIP4 ProductType=1 (RemoteIP=172.16.0.0/12 OR RemoteIP=192.168.0.0/16 OR RemoteIP=10.0.0.0/8)
| where RPort<10000
| eval Protocol_decimal=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP") 
| stats dc(aid) as uniqueEndpoints count(aid) as totalConnections by RPort, Protocol_decimal
| rename RPort as remotePort, Protocol_decimal as Protocol
| sort +Protocol -uniqueEndpoints
```

## Query 10
```cql
| where RPort<10000
```

## Query 11
```cql
| eval Protocol_decimal=case(Protocol_decimal=1, "ICMP", Protocol_decimal=6, "TCP", Protocol_decimal=17, "UDP", Protocol_decimal=58, "IPv6-ICMP")
```

## Query 12
```cql
| stats dc(aid) as uniqueEndpoints count(aid) as totalConnections by RPort, Protocol_decimal
```

## Query 13
```cql
| rename RPort as remotePort, Protocol_decimal as Protocol
```

## Query 14
```cql
| sort +Protocol -uniqueEndpoints
```
