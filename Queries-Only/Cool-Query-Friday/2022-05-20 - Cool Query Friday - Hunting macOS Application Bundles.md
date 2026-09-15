---
title: "Hunting macOS Application Bundles"
date: 2022-05-20
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/utycmg/20220520_cool_query_friday_hunting_macos/"
mitre: []
series: Cool Query Friday
---

# Hunting macOS Application Bundles

> Source: [https://www.reddit.com/r/crowdstrike/comments/utycmg/20220520_cool_query_friday_hunting_macos/](https://www.reddit.com/r/crowdstrike/comments/utycmg/20220520_cool_query_friday_hunting_macos/) — by Andrew-CS (CrowdStrike) — 2022-05-20

Welcome to our forty-fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
[...]
| regex TargetFileName=".*\/.*\.app\/.*"
```

## Query 2
```cql
[...]
| rex field=TargetFileName ".*\/(?<appName>.*\.app)\/.*" 
| rex field=TargetFileName "(?<filePath>^\/.*\.app)\/.*"
```

## Query 3
```cql
[...]
| eval fileLocale=case(match(TargetFileName,"^\/Applications\/"), "Applications Folder", match(TargetFileName,"^\/Users\/"), "User's Home Folder", match(TargetFileName,"^\/(System|Library|Developer)\/"), "macOS Core Folder")
```

## Query 4
```cql
[...]
| rex field=TargetFileName "\/Users\/\w+\/(?<homeFolderLocale>\w+)\/.*"
| eval homeFolderLocale = "~/".homeFolderLocale
| fillnull value="-" homeFolderLocale
```

## Query 5
```cql
[...]
| stats dc(aid) as endpointCount, dc(TargetFileName) as filesWritten, dc(SHA256HashData) as sha256Count by appName, filePath, fileLocale, homeFolderLocale
| sort - endpointCount
```

## Query 6
```cql
event_platform=mac event_simpleName=MachOFileWritten 
| regex TargetFileName=".*\/.*\.app\/.*" 
| rex field=TargetFileName ".*\/(?<appName>.*\.app)\/.*" 
| rex field=TargetFileName "(?<filePath>^\/.*\.app)\/.*" 
| eval fileLocale=case(match(TargetFileName,"^\/Applications\/"), "Applications Folder", match(TargetFileName,"^\/Users\/"), "User's Home Folder", match(TargetFileName,"^\/(System|Library|Developer)\/"), "macOS Core Folder")
| rex field=TargetFileName "\/Users\/\w+\/(?<homeFolderLocale>\w+)\/.*"
| eval homeFolderLocale = "~/".homeFolderLocale
| fillnull value="-" homeFolderLocale
| stats dc(aid) as endpointCount, dc(TargetFileName) as filesWritten, dc(SHA256HashData) as sha256Count by appName, filePath, fileLocale, homeFolderLocale
| sort - endpointCount
```
