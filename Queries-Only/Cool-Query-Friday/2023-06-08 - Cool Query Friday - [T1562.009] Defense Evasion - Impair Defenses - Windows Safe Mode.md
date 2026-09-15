---
title: "[T1562.009] Defense Evasion - Impair Defenses - Windows Safe Mode"
date: 2023-06-08
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/144f19i/20230608_cool_query_friday_t1562009_defense/"
mitre: [T1562, T1562.009]
series: Cool Query Friday
---

# [T1562.009] Defense Evasion - Impair Defenses - Windows Safe Mode

> Source: [https://www.reddit.com/r/crowdstrike/comments/144f19i/20230608_cool_query_friday_t1562009_defense/](https://www.reddit.com/r/crowdstrike/comments/144f19i/20230608_cool_query_friday_t1562009_defense/) — by Andrew-CS (CrowdStrike) — 2023-06-08

Welcome to our fifty-seventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
#event_simpleName=ProcessRollup2 event_platform=Win CommandLine=/safeboot/i  
| ImageFileName=/\\(?<FileName>\w+\.exe)$/i
| default(value="N/A", field=[GrandParentBaseFileName])
| groupBy([GrandParentBaseFileName, ParentBaseFileName, FileName], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount), collect([CommandLine])]))
```

## Query 2
```cql
event_platform=Win event_simpleName=ProcessRollup2 "bcdedit" "safeboot"
| fillnull value="-" GrandParentBaseFileName
| stats dc(aid) as uniqueEndpoints, count(aid) as executionCount, values(CommandLine) as CommandLine by GrandParentBaseFileName, ParentBaseFileName, FileName
```

## Query 3
```cql
#event_simpleName=ProcessRollup2 event_platform=Win (ImageFileName=/\\bcdedit\.exe/i OR CommandLine=/bcdedit/i)
| ImageFileName=/\\(?<FileName>\w+\.exe)$/i
| default(value="N/A", field=[GrandParentBaseFileName])
| groupBy([GrandParentBaseFileName, ParentBaseFileName, FileName], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount), collect([CommandLine])]))
```

## Query 4
```cql
event_platform=Win event_simpleName=ProcessRollup2 "bcdedit" 
| fillnull value="-" GrandParentBaseFileName
| stats dc(aid) as uniqueEndpoints, count(aid) as executionCount, values(CommandLine) as CommandLine by GrandParentBaseFileName, ParentBaseFileName, FileName
```

## Query 5
```cql
#event_simpleName=ProcessRollup2 event_platform=Win (ImageFileName=/\\bcdedit\.exe/i OR CommandLine=/bcdedit/i)
| ImageFileName=/\\(?<FileName>\w+\.exe)$/i
// Begin scoring. Adjust searches and values as desired.
| case{
   CommandLine=/\/set/i | scoreSet := 5;
   *;
   }
| case {
   CommandLine=/\/delete/i | scoreDelete := 5;
   *;
   }
| case {
   CommandLine=/safeboot/i | scoreSafeBoot := 10;
   *;
   }
| case {
   CommandLine=/network/i | scoreNetwork := 20;
   *;
   }
| case {
   CommandLine=/\{[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}[\}]/ | scoreGUID := 9;
   *;
}
| case {
   ParentBaseFileName=/^(powershell|cmd)\.exe$/i | scoreParent := "7";
   *;
   }
// End scoring
| default(value="N/A", field=[GrandParentBaseFileName])
| default(value=0, field=[scoreSet, scoreDelete, scoreSafeBoot, scoreNetwork, scoreGUID, scoreParent])
| totalScore := scoreSet + scoreDelete + scoreSafeBoot + scoreNetwork + scoreGUID + scoreParent
| groupBy([GrandParentBaseFileName, ParentBaseFileName, FileName, CommandLine], function=([collect(totalScore), count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=executionCount)]))
| select([GrandParentBaseFileName, ParentBaseFileName, FileName, totalScore, uniqueEndpoints, executionCount, CommandLine])
| sort(totalScore, order=desc, limit=1000)
```

## Query 6
```cql
event_platform=Win event_simpleName=ProcessRollup2 "bcdedit" 
| fillnull value="-" GrandParentBaseFileName
| eval scoreSet=if(match(CommandLine,"\/set"),"5","0") 
| eval scoreDelete=if(match(CommandLine,"\/delete"),"5","0") 
| eval scoreSafeBoot=if(match(CommandLine,"safeboot"),"10","0") 
| eval scoreNetwork=if(match(CommandLine,"network"),"20","0") 
| eval scoreGUID=if(match(CommandLine,"{[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}[}]"),"9","0") 
| eval scoreParent=if(match(ParentBaseFileName,"^(powershell|cmd)\.exe"),"7","0") 
| eval totalScore=scoreSet+scoreDelete+scoreSafeBoot+scoreNetwork+scoreGUID+scoreParent
| stats dc(aid) as uniqueEndpoints, count(aid) as executionCount, values(CommandLine) as CommandLine by GrandParentBaseFileName, ParentBaseFileName, FileName, totalScore
| sort 0 - totalScore
```
