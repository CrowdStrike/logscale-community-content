---
title: "FileVault Status in macOS"
date: 2021-10-01
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/pz7i14/20211001_cool_query_friday_filevault_status_in/"
mitre: []
series: Cool Query Friday
---

# FileVault Status in macOS

> Source: [https://www.reddit.com/r/crowdstrike/comments/pz7i14/20211001_cool_query_friday_filevault_status_in/](https://www.reddit.com/r/crowdstrike/comments/pz7i14/20211001_cool_query_friday_filevault_status_in/) — by Andrew-CS (CrowdStrike) — 2021-10-01

Welcome to our twenty-fifth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=mac event_simpleName=FileVaultStatus
| fields aid, FileVaultIsEnabled_decimal
```

## Query 2
```cql
event_platform=mac event_simpleName=FileVaultStatus
| fields aid, FileVaultIsEnabled_decimal
| eval fvStatus=case(FileVaultIsEnabled_decimal=1, "ENABLED", FileVaultIsEnabled_decimal=0, "DISABLED")
```

## Query 3
```cql
event_platform=mac event_simpleName=FileVaultStatus
| fields aid, FileVaultIsEnabled_decimal
| eval fvStatus=case(FileVaultIsEnabled_decimal=1, "ENABLED", FileVaultIsEnabled_decimal=0, "DISABLED")
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Country, Timezone, FirstSeen
```

## Query 4
```cql
event_platform=mac event_simpleName=FileVaultStatus
| fields aid, FileVaultIsEnabled_decimal
| eval fvStatus=case(FileVaultIsEnabled_decimal=1, "ENABLED", FileVaultIsEnabled_decimal=0, "DISABLED")
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Country, Timezone, FirstSeen
| stats latest(fvStatus) as fvStatus by aid, ComputerName, Version, Country, Timezone, FirstSeen
| convert ctime(FirstSeen) as "falconInstallTime"
```

## Query 5
```cql
event_platform=mac (event_simpleName=FileVaultStatus OR event_simpleName=AgentOnline OR event_simpleName=UserLogon)
| fields aid, aip, FileVaultIsEnabled_decimal, SystemSerialNumber, UserPrincipal
| eval fvStatus=case(FileVaultIsEnabled_decimal=1, "ENABLED", FileVaultIsEnabled_decimal=0, "DISABLED")
```

## Query 6
```cql
[...]
| eval SystemSerialNumber=upper(SystemSerialNumber)
| eval UserPrincipal=lower(UserPrincipal)
| stats latest(aip) as aip, latest(fvStatus) as fvStatus, values(SystemSerialNumber) as serialNumber, values(UserPrincipal) as endpointLogons by aid
| where isnotnull(fvStatus)
```

## Query 7
```cql
[...]
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Country, Timezone, FirstSeen
```

## Query 8
```cql
[...]
| iplocation aip
```

## Query 9
```cql
[...]
| table aid, ComputerName, serialNumber, fvStatus, aip, Country, Region, City, Timezone, Version, endpointLogons, FirstSeen
```

## Query 10
```cql
[...]
| convert ctime(FirstSeen)
| rename aid as "Falcon Agent ID", ComputerName as "Mac Hostname", serialNumber as "Serial Number", fvStatus as "FileVault", aip as "External IP", Version as "macOS Version", endpointLogons as "User Logons", FirstSeen as "Falcon Install Date"
```

## Query 11
```cql
event_platform=mac (event_simpleName=FileVaultStatus OR event_simpleName=AgentOnline OR event_simpleName=UserLogon)
| fields aid, aip, FileVaultIsEnabled_decimal, SystemSerialNumber, UserPrincipal 
| eval fvStatus=case(FileVaultIsEnabled_decimal=1, "ENABLED", FileVaultIsEnabled_decimal=0, "DISABLED")
| eval SystemSerialNumber=upper(SystemSerialNumber)
| eval UserPrincipal=lower(UserPrincipal)
| stats latest(aip) as aip, latest(fvStatus) as fvStatus, values(SystemSerialNumber) as serialNumber, values(UserPrincipal) as endpointLogons by aid
| where isnotnull(fvStatus)
| lookup local=true aid_master aid OUTPUT ComputerName, Version, Country, Timezone, FirstSeen
| iplocation aip
| table aid, ComputerName, serialNumber, fvStatus, aip, Country, Region, City, Timezone, Version, endpointLogons, FirstSeen
| convert ctime(FirstSeen)
| rename aid as "Falcon Agent ID", ComputerName as "Mac Hostname", serialNumber as "Serial Number", fvStatus as "FileVault", aip as "External IP", Version as "macOS Version", endpointLogons as "User Logons", FirstSeen as "Falcon Install Date"
```
