---
title: "ATT&CK Edition: T1087.004"
date: 2023-11-10
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/17s63ri/20231110_cool_query_friday_attck_edition_t1087004/"
mitre: [T1087, T1087.001, T1087.002, T1087.003, T1087.004]
series: Cool Query Friday
---

# ATT&CK Edition: T1087.004

> Source: [https://www.reddit.com/r/crowdstrike/comments/17s63ri/20231110_cool_query_friday_attck_edition_t1087004/](https://www.reddit.com/r/crowdstrike/comments/17s63ri/20231110_cool_query_friday_attck_edition_t1087004/) — by Andrew-CS (CrowdStrike) — 2023-11-10

Welcome to our sixty-seventh installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval Description=case(match(CommandLine,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in command line invocation.", match(CommandHistory,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in command line history.", match(ScriptContent,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in script contents.")
```

## Query 2
```cql
| eval Details=coalesce(CommandLine, CommandHistory, ScriptContent)
```

## Query 3
```cql
| table _time, ComputerName, aid, UserName, UserSid_readable, TargetProcessId_decimal, Description, Details
```

## Query 4
```cql
| eval GraphExplorer=case(TargetProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . TargetProcessId_decimal)

*Public Cloud Tools*
```

## Query 5
```cql
event_simpleName=ProcessRollup2 ("az" OR "aws" OR "gcloud")
    | regex CommandLine="(az\s+ad\s+user\s+list|aws\s+iam\s+list\-(roles|users)|gcloud\s+ (iam\s+service\-accounts\s+list|projects\s+get\-iam\-policy))"
```

## Query 6
```cql
| table _time, ComputerName, aid, UserName, UserSid_readable, TargetProcessId_decimal, FileName, CommandLine
```

## Query 7
```cql
// Search for PowerShell Commandlet Invocations that Enumerate Office365 Role Membership
#event_simpleName=/^(ProcessRollup2$|CommandHistory$|ScriptControl)/ event_platform=Win /Get-MsolRoleMember/
// Concatenate fields of interest from events of interest
| Details:=concat([CommandHistory,CommandLine,ScriptContent])
// Create "Description" field based on location of target string
| case {
#event_simpleName=CommandHistory AND CommandHistory=/(Get-MsolRoleMember)/i | Description:="T1087.004 discovered in command line history.";
#event_simpleName=ProcessRollup2 AND CommandLine=/(Get-MsolRoleMember)/i | Description:="T1087.004 discovered in command line invocation.";
#event_simpleName=/^ScriptControl/ AND ScriptContent=/(Get-MsolRoleMember)/i | Description:="T1087.004 discovered in script contents.";
* | Description:="T1087.003 discovered in general event telemetry.";
}
// Format output into table
| select([@timestamp, ComputerName, aid, UserName, UserSid, TargetProcessId, Description, Details])
// Add link to Graph Explorer
| format("[Graph Explorer](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "TargetProcessId"], as="Graph Explorer")
```

## Query 8
```cql
// Search for public cloud command line tool invocation
(#event_simpleName=ProcessRollup2 CommandLine=/az\s+ad\s+user\s+list/i) OR (#event_simpleName=ProcessRollup2 CommandLine=/aws\s+iam\s+list\-(roles|users)/i) OR (#event_simpleName=ProcessRollup2 CommandLine=/gcloud\s+ (iam\s+service\-accounts\s+list|projects\s+get\-iam\-policy)/i)
// Format output into table
| select([@timestamp, ComputerName, aid, UserName, UserSid, TargetProcessId, FileName, CommandLine])
// Add link to Graph Explorer
| format("[Graph Explorer](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "TargetProcessId"], as="Graph Explorer")
```

## Query 9
```cql
```Get events in scope for T1087.004```
event_simpleName IN (ProcessRollup2, CommandHistory, ScriptControl*) event_platform=Win "Get-MsolRoleMember"
```Create "Description" field based on location of target string```
| eval Description=case(match(CommandLine,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in command line invocation.", match(CommandHistory,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in command line history.", match(ScriptContent,".*(Get-MsolRoleMember).*"), "T1087.004 discovered in script contents.")
```Concat fields of interest from events of interest```
| eval Details=coalesce(CommandLine, CommandHistory, ScriptContent)
```Format output into table```
| table _time, ComputerName, aid, UserName, UserSid_readable, TargetProcessId_decimal, Description, Details
```Add link to Graph Explorer```
| eval GraphExplorer=case(TargetProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . TargetProcessId_decimal)
```

## Query 10
```cql
```Search for public cloud command line tool invocation```
event_simpleName=ProcessRollup2 ("az" OR "aws" OR "gcloud")
| regex CommandLine="(az\s+ad\s+user\s+list|aws\s+iam\s+list\-(roles|users)|gcloud\s+ (iam\s+service\-accounts\s+list|projects\s+get\-iam\-policy))"
```Format output into table```
| table _time, ComputerName, aid, UserName, UserSid_readable, TargetProcessId_decimal, FileName, CommandLine
```Add link to Graph Explorer```
| eval GraphExplorer=case(TargetProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . TargetProcessId_decimal)
```
