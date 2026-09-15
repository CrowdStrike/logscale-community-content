---
title: "[T1036.005] Inventorying LOLBINs and Hunting for System Folder Binary Masquerading"
date: 2023-08-11
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/15oa5io/20230811_cool_query_friday_t1036005_inventorying/"
mitre: [T1036, T1036.005]
series: Cool Query Friday
---

# [T1036.005] Inventorying LOLBINs and Hunting for System Folder Binary Masquerading

> Source: [https://www.reddit.com/r/crowdstrike/comments/15oa5io/20230811_cool_query_friday_t1036005_inventorying/](https://www.reddit.com/r/crowdstrike/comments/15oa5io/20230811_cool_query_friday_t1036005_inventorying/) — by Andrew-CS (CrowdStrike) — 2023-08-11

Welcome to our sixty-first installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName=/\\Windows\\(System32|SysWOW64)\\/
```

## Query 2
```cql
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
```

## Query 3
```cql
| FileName:=lower(FileName)
```

## Query 4
```cql
| lower(field=FileName, as=FileName)
```

## Query 5
```cql
| groupBy([FileName, FilePath], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount)]))
```

## Query 6
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| lower(field=FileName, as=FileName)
| groupBy([FileName, FilePath], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount)]))
```

## Query 7
```cql
| uniqueEndpoints:=format("%,.0f",field="uniqueEndpoints")
| executionCount:=format("%,.0f",field="executionCount")
```

## Query 8
```cql
| expectedFileName:=rename(field="FileName")
| expectedFilePath:=rename(field="FilePath")
```

## Query 9
```cql
| details:=format(format="The file %s has been executed %s time on %s unique endpoints in the past 30 days.\nThe expected file path for this binary is: %s.", field=[expectedFileName, executionCount, uniqueEndpoints, expectedFilePath])
| select([expectedFileName, expectedFilePath, uniqueEndpoints, executionCount, details])
```

## Query 10
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| lower(field=FileName, as=FileName)
| groupBy([FileName, FilePath], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount)]))
| uniqueEndpoints:=format("%,.0f",field="uniqueEndpoints")
| executionCount:=format("%,.0f",field="executionCount")
| expectedFileName:=rename(field="FileName")
| expectedFilePath:=rename(field="FilePath")
| details:=format(format="The file %s has been executed %s time on %s unique endpoints in the past 30 days.\nThe expected file path for this binary is: %s.", field=[expectedFileName, executionCount, uniqueEndpoints, expectedFilePath])
| select([expectedFileName, expectedFilePath, uniqueEndpoints, executionCount, details])
```

## Query 11
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| lower(field=FileName, as=FileName)
```

## Query 12
```cql
| FileName =~ match(file="win-sys-folder-inventory.csv", column=expectedFileName, strict=true)
```

## Query 13
```cql
| groupBy([FileName], function=([count(aid, as=executionCount), count(aid, distinct=true, as=endpointCount), collect([FilePath, details])]))
```

## Query 14
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| lower(field=FileName, as=FileName)
| FileName =~ match(file="win-sys-folder-inventory.csv", column=expectedFileName, strict=true)
| groupBy([FileName], function=([count(aid, as=executionCount), count(aid, distinct=true, as=endpointCount), collect([FilePath, details])]))
```

## Query 15
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| FilePath!=/[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}/
```

## Query 16
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(System32|SysWOW64)\\/
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
| FilePath!=/[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}/
| lower(field=FileName, as=FileName)
| !in(field="FileName", values=["onedrivesetup.exe"])
```

## Query 17
```cql
| !in(field="FileName", values=["onedrivesetup.exe", "myCustomApp.exe"])
```

## Query 18
```cql
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(UUS|System32|SysWOW64)\\/
```

## Query 19
```cql
| test(executionCount < 30)
```

## Query 20
```cql
// Get all process execution events ocurring ourside of the system folder.
#event_simpleName=/^(ProcessRollup2|SyntheticProcessRollup2)$/ event_platform=Win ImageFileName!=/\\Windows\\(UUS|System32|SysWOW64)\\/
// Create fields FilePath and FileName from ImageFileName.
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<FilePath>\\.+\\)(?<FileName>.+$)/
// Omit all file paths with GUID. Optional.
| FilePath!=/[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}/
// Force field FileName to lower case.
| FileName:=lower(field=FileName)
// Include file names to be omitted. Optional.
| !in(field="FileName", values=["onedrivesetup.exe", "mycustomApp.exe"])
// Check events above against system folder inventory. Remove non-matches. Output all columns from lookup file.
| FileName =~ match(file="win-sys-folder-inventory.csv", column=expectedFileName, strict=true)
// Group matches by FileName value.
| groupBy([FileName], function=([count(aid, as=executionCount), count(aid, distinct=true, as=endpointCount), collect([FilePath, expectedFilePath, details])]))
// Set threshold after which results are dropped. Optional.
| test(executionCount < 30)
```
