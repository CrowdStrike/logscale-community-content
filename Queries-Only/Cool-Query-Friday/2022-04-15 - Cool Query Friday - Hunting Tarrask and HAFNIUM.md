---
title: "Hunting Tarrask and HAFNIUM"
date: 2022-04-15
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/u49jxq/20220415_cool_query_friday_hunting_tarrask_and/"
mitre: []
series: Cool Query Friday
---

# Hunting Tarrask and HAFNIUM

> Source: [https://www.reddit.com/r/crowdstrike/comments/u49jxq/20220415_cool_query_friday_hunting_tarrask_and/](https://www.reddit.com/r/crowdstrike/comments/u49jxq/20220415_cool_query_friday_hunting_tarrask_and/) — by Andrew-CS (CrowdStrike) — 2022-04-15

Welcome to our forty-second installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
[...]
| search AuthenticationId_decimal=999
```

## Query 2
```cql
[...]
| search RegObjectName="\\REGISTRY\\MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\*"
```

## Query 3
```cql
[...]
| search RegOperationType_decimal IN (2, 4) AND RegValueName="SD"
```

## Query 4
```cql
event_platform=win event_simpleName IN (AsepValueUpdate, RegGenericValueUpdate) 
| search AuthenticationId_decimal=999
| search RegObjectName="\\REGISTRY\\MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\*"
| search RegOperationType_decimal IN (2, 4) AND RegValueName="SD"
```

## Query 5
```cql
[...]
| rename RegOperationType_decimal as RegOperationType, AsepClass_decimal as AsepClass
| lookup local=true RegOperation.csv RegOperationType OUTPUT RegOperationName
| lookup local=true AsepClass.csv AsepClass OUTPUT AsepClassName
| eval ProcExplorer=case(ContextProcessId_decimal!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . ContextProcessId_decimal)
```

## Query 6
```cql
[...]
| table aid, ComputerName, RegObjectName, RegValueName, AsepClassName, RegOperationName, ProcExplorer
```

## Query 7
```cql
event_platform=win event_simpleName IN (AsepValueUpdate, RegGenericValueUpdate) 
| search AuthenticationId_decimal=999
| search RegObjectName="\\REGISTRY\\MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\*"
| search RegOperationType_decimal IN (2, 4) AND RegValueName="SD"
| rename RegOperationType_decimal as RegOperationType, AsepClass_decimal as AsepClass
| lookup local=true RegOperation.csv RegOperationType OUTPUT RegOperationName
| lookup local=true AsepClass.csv AsepClass OUTPUT AsepClassName
| eval ProcExplorer=case(ContextProcessId_decimal!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . ContextProcessId_decimal)
| table aid, ComputerName, RegObjectName, RegValueName, AsepClassName, RegOperationName, ProcExplorer
```

## Query 8
```cql
event_platform=win event_simpleName IN (AsepValueUpdate, RegGenericValueUpdate) 
| search AuthenticationId_decimal=999
| search RegOperationType_decimal IN (2, 4)
| rename RegOperationType_decimal as RegOperationType, AsepClass_decimal as AsepClass
| lookup local=true RegOperation.csv RegOperationType OUTPUT RegOperationName
| lookup local=true AsepClass.csv AsepClass OUTPUT AsepClassName
| eval ProcExplorer=case(ContextProcessId_decimal!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . ContextProcessId_decimal)
| table aid, ComputerName, RegObjectName, RegValueName, AsepClassName, RegOperationName, ProcExplorer
```
