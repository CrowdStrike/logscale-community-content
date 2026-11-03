---
title: "Tagging and Tracking Lost Endpoints"
date: 2021-11-12
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/qsbtnp/20211112_cool_query_friday_tagging_and_tracking/"
mitre: []
series: Cool Query Friday
---

# Tagging and Tracking Lost Endpoints

> Source: [https://www.reddit.com/r/crowdstrike/comments/qsbtnp/20211112_cool_query_friday_tagging_and_tracking/](https://www.reddit.com/r/crowdstrike/comments/qsbtnp/20211112_cool_query_friday_tagging_and_tracking/) — by Andrew-CS (CrowdStrike) — 2021-11-12

Welcome to our thirty-first installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
| inputlookup aid_master
| table aid ComputerName *Tags
```

## Query 2
```cql
[...]
| lookup local=true aid_master aid OUTPUT FalconGroupingTags
```

## Query 3
```cql
[...]
| search FalconGroupingTags!="none" AND FalconGroupingTags!="-"
| makemv delim=";" FalconGroupingTags
| search FalconGroupingTags="FalconGroupingTags\Group2"
```

## Query 4
```cql
index=main sourcetype=AgentConnect* event_simpleName=AgentConnect 
| lookup local=true aid_master aid OUTPUT FalconGroupingTags 
| search FalconGroupingTags!="none" AND FalconGroupingTags!="-" 
| makemv delim=";" FalconGroupingTags 
| search FalconGroupingTags="FalconGroupingTags/Group2"
| fields aid, aip, ComputerName, ConnectTime_decimal, FalconGroupingTags
```

## Query 5
```cql
[...]
| iplocation aip
```

## Query 6
```cql
[...]
| stats count(aid) as totalConnections, earliest(ConnectTime_decimal) as firstConnect, latest(ConnectTime_decimal) as lastConnect by aid, ComputerName, aip, City, Region, Country
| convert ctime(firstConnect) ctime(lastConnect)
```

## Query 7
```cql
[...]
| sort +ComputerName, +firstConnect
| rename aid as "Falcon Agent ID", ComputerName as "Lost System", aip as "External IP", totalConnections as "Connections from IP", firstConnect as "First Connection", lastConnect as "Last Connection"
```
