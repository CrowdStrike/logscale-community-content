---
title: "Hunting PE Language ID Prevalence in PeVersionInfo"
date: 2023-01-06
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/104y1wr/20230106_cool_query_friday_hunting_pe_language_id/"
mitre: []
series: Cool Query Friday
---

# Hunting PE Language ID Prevalence in PeVersionInfo

> Source: [https://www.reddit.com/r/crowdstrike/comments/104y1wr/20230106_cool_query_friday_hunting_pe_language_id/](https://www.reddit.com/r/crowdstrike/comments/104y1wr/20230106_cool_query_friday_hunting_pe_language_id/) — by Andrew-CS (CrowdStrike) — 2023-01-06

Happy New Year and welcome to our fifty-fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
event_simpleName=PeVersionInfo event_platform=win
| stats dc(aid) as uniqueEndpoints by LanguageId_decimal
| sort 0 -uniqueEndpoints
```

## Query 2
```cql
#event_simpleName=PeVersionInfo event_platform=Win
| groupBy("LanguageId")
| sort(_count, order=desc, limit=100)
```

## Query 3
```cql
#event_simpleName=PeVersionInfo event_platform=Win 
| !in(LanguageId, values=[0, 1033])
```

## Query 4
```cql
event_simpleName=PeVersionInfo event_platform=win NOT LanguageId_decimal IN (1033, 0)
| rex field=FilePath "(\\\\Device\\\\HarddiskVolume\d+)?(?<trimmedFilePath>.*)"
| stats count(aid) as uniqueEndpoints, values(FileName) as fileNames, values(trimmedFilePath) as filePaths by SHA256HashData, LanguageId_decimal
| sort 0 -occurrences
```

## Query 5
```cql
#event_simpleName=PeVersionInfo event_platform=Win 
| !in(LanguageId, values=[0, 1033])
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<filePath>\\.*)\\(?<fileName>.+\.\w+)$/i
| groupBy([SHA256HashData, LanguageId], function=([count(aid, distinct=true, as=uniqueEndpoints), collect([fileName, filePath])]))
| sort(uniqueEndpoints, order=desc, limit=500)
```

## Query 6
```cql
event_simpleName=PeVersionInfo event_platform=win NOT LanguageId_decimal IN (1033, 0)
| rex field=FilePath "(\\\\Device\\\\HarddiskVolume\d+)?(?<trimmedFilePath>.*)"
| search "Users"
| regex trimmedFilePath!=".*\\\(Google|boot\\efi)\\\.*"
| regex FileName!=".*\.LocalizedResources\..*"
| stats count(aid) as uniqueEndpoints, values(FileName) as fileNames, values(trimmedFilePath) as filePaths by SHA256HashData, LanguageId_decimal
| sort -occurrences
```

## Query 7
```cql
#event_simpleName=PeVersionInfo event_platform=Win 
| !in(LanguageId, values=[0, 1033])
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<filePath>\\.*)\\(?<fileName>.+\.\w+)$/i
| filePath=/\\Users\\/i
| filePath!=/\\(Google|\\boot\\efi|OneDrive)\\/i
| groupBy([SHA256HashData, LanguageId], function=([count(aid, distinct=true, as=uniqueEndpoints), collect([fileName, filePath])]))
| sort(uniqueEndpoints, order=desc, limit=500)
```

## Query 8
```cql
[...]
| where uniqueEndpoints < 10
```

## Query 9
```cql
[...]
| test(uniqueEndpoints < 10)
```

## Query 10
```cql
event_simpleName=PeVersionInfo event_platform=win NOT LanguageId_decimal IN (1033, 0)
| rex field=FilePath "(\\\\Device\\\\HarddiskVolume\d+)?(?<trimmedFilePath>.*)"
| search "Users"
| regex trimmedFilePath!=".*\\\(Google|boot\\efi)\\\.*"
| regex FileName!=".*\.LocalizedResources\..*"
| stats count(aid) as uniqueEndpoints, values(FileName) as fileNames, values(OriginalFilename) as originalFileNames, values(trimmedFilePath) as filePaths by SHA256HashData, LanguageId_decimal
| sort -occurrences 
| lookup local=true LanguageId.csv LanguageId_decimal OUTPUT lcid_lang, lcid_string
| table SHA256HashData, fileNames, originalFileNames, filePaths, uniqueEndpoints, LanguageId_decimal, lcid_lang, lcid_string
| rename SHA256HashData as SHA256, fileNames as "File Names", originalFileNames as "Original FileNames", filePaths as "File Paths", uniqueEndpoints as "Endpoints", LanguageId_decimal as "Language ID", lcid_lang as "LCID Code", lcid_string as "LCID String"
```

## Query 11
```cql
#event_simpleName=PeVersionInfo event_platform=Win 
| !in(LanguageId, values=[0, 1033])
| ImageFileName=/(\\Device\\HarddiskVolume\d+)?(?<filePath>\\.*)\\(?<fileName>.+\.\w+)$/i
| filePath=/\\Users\\/i
| filePath!=/\\(Google|\\boot\\efi|OneDrive)\\/i
| groupBy([SHA256HashData, LanguageId], function=([count(aid, distinct=true, as=uniqueEndpoints), collect([fileName, OriginalFilename, filePath])]))
| sort(uniqueEndpoints, order=desc, limit=500)
| match(file="LanguageId.csv", field=LanguageId, ignoreCase=true, strict=false)
| select([SHA256HashData, fileName, OriginalFilename, filePath, uniqueEndpoints, LanguageId, lcid_lang, lcid_string])
| rename("SHA256HashData",as="SHA256")
| rename("fileName",as="File Names")
| rename("OriginalFilename",as="Original File Names")
| rename("filePath",as="Paths")
| rename("LanguageId",as="Language ID")
| rename("lcid_lang",as="LCID Code")
| rename("lcid_string",as="LCID String")
```
