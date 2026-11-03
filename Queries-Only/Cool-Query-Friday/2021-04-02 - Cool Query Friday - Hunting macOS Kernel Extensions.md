---
title: "Hunting macOS Kernel Extensions"
date: 2021-04-02
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/mijvb0/20210402_cool_query_friday_hunting_macos_kernel/"
mitre: []
series: Cool Query Friday
---

# Hunting macOS Kernel Extensions

> Source: [https://www.reddit.com/r/crowdstrike/comments/mijvb0/20210402_cool_query_friday_hunting_macos_kernel/](https://www.reddit.com/r/crowdstrike/comments/mijvb0/20210402_cool_query_friday_hunting_macos_kernel/) — by Andrew-CS (CrowdStrike) — 2021-04-02

Welcome to our fifth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=mac event_simpleName=KextLoad 
| stats dc(aid) as systemCount by BundleID
| sort - systemCount
```

## Query 2
```cql
kextstat | grep -v com.apple
```

## Query 3
```cql
event_platform=mac event_simpleName=KextLoad 
| lookup aid_master aid OUTPUT Version
```

## Query 4
```cql
event_platform=mac event_simpleName=KextLoad 
| lookup aid_master aid OUTPUT Version
| rex field=Version "^(?<osVersion>[^.]*)\("
```

## Query 5
```cql
event_platform=mac event_simpleName=KextLoad 
| lookup aid_master aid OUTPUT Version
| rex field=Version "^(?<osVersion>[^.]*)\("
| stats dc(aid) as systemCount by BundleID, osVersion
| sort - systemCount
```

## Query 6
```cql
event_platform=mac event_simpleName=KextLoad 
| search BundleID!=com.apple.*
| lookup aid_master aid OUTPUT Version
| rex field=Version "^(?<osVersion>[^.]*)\("
| fillnull osVersion value="Unknown"
| stats dc(aid) as systemCount by BundleID, osVersion
| sort - systemCount
```

## Query 7
```cql
event_platform=mac event_simpleName=KextLoad 
| search BundleID!=com.apple.* 
| lookup aid_master aid OUTPUT Version, SystemProductName
| rex field=Version "^(?<osVersion>[^.]*)\("
| fillnull osVersion value="Unknown"
| stats values(ComputerName) as endpointName dc(BundleID) as nonAppleKernelCount values(BundleID) as nonAppleKernelExt by aid, osVersion, SystemProductName
| sort - nonAppleKernelCount
```

## Query 8
```cql
event_platform=mac event_simpleName=ProcessRollup2 MachOSubType_decimal=5 FilePath="/Applications/*" 
| stats  dc(aid) as systemCount count(aid) as executionCount by FileName SHA256HashData   
| lookup  local=true appinfo.csv SHA256HashData OUTPUT ProductName , ProductVersion , FileDescription , FileVersion , CompanyName  
 sort  - systemCount
```
