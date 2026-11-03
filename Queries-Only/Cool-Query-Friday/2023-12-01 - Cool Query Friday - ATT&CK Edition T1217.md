---
title: "ATT&CK Edition: T1217"
date: 2023-12-01
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/188e5ci/20231201_cool_query_friday_attck_edition_t1217/"
mitre: [T1010, T1087, T1087.001, T1087.002, T1087.003, T1087.004, T1217]
series: Cool Query Friday
---

# ATT&CK Edition: T1217

> Source: [https://www.reddit.com/r/crowdstrike/comments/188e5ci/20231201_cool_query_friday_attck_edition_t1217/](https://www.reddit.com/r/crowdstrike/comments/188e5ci/20231201_cool_query_friday_attck_edition_t1217/) — by Andrew-CS (CrowdStrike) — 2023-12-01

Welcome to our sixty-ninth (not saying a word) installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval BrowserTarget=case(match(Details,"(?i).*\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User\sData\\\\Default.*"), "Windows - Google Chrome", match(Details,"(?i).*\/Users\/.+\/Library\/Application\sSupport\/Google\/Chrome\/Default.*"), "macOS - Google Chrome", match(Details,"(?i).*\/home\/.+\/\.config\/google\-chrome\/Default.*"), "Linux - Google Chrome")
```

## Query 2
```cql
| eval Location=case(match(event_simpleName,"ProcessRollup2"), "Process Execution - Command Line", match(event_simpleName,"CommandHistory"), "Process Execution - Command History", match(event_simpleName,"^ScriptControl.*"), "Script - Script Contents")
```

## Query 3
```cql
| eval ShortDetails=substr(Details,1,100)
```

## Query 4
```cql
| stats dc(aid) as UniqueEndpoints, count(aid) as ExecutionCount, last(aid) as aid, last(falconPID) as falconPID by event_platform, BrowserTarget, Location, ShortDetails
```

## Query 5
```cql
| where UniqueEndpoints < 50
```

## Query 6
```cql
| eval LastExecution=case(falconPID!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . falconPID)
```

## Query 7
```cql
// Get events of interest for T1217
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/

// Omit events where the browser is the executing process
| FileName!="chrome*"

// Normalize details field
| Details:=concat([CommandLine, CommandHistory,ScriptContent])

// Further narrow events with brute force search against Details field
| Details=/chrome/i

// Normalize Falcon UPID value
| falconPID:=TargetProcessId | falconPID:=ContextProcessId

// Check to see which operating system is being targeted
| case {
   Details=/\\AppData\\Local\\Google\\Chrome\\User\sData\\Default/i                | BrowserTarget:="Windows - Google Chrome";
   Details=/\/Users\/\S+\/Library\/Application\sSupport\/Google\/Chrome\/Default/i | BrowserTarget:="macOS - Google Chrome";
   Details=/\/home\/\S+\/\.config\/google\-chrome\/Default\//i                     | BrowserTarget:="Linux - Google Chrome"; 
}

// Check to see where targeting is found
| case {
   #event_simpleName=ProcessRollup2   | Location:="Process Execution - Command Line";
   #event_simpleName=CommandHistory   | Location:="Process Execution - Command History";
   #event_simpleName=/^ScriptControl/ | Location:="Script - Script Contents"; 
}

// Calculate hash for details field for use in groupBy statement
| DetailsHash:=hash(field=Details)

// Created shortened Details field of 100 characters to improve readability
| ShortDetails:=format("%,.100s", field=Details)

//Aggregate results
| groupBy([event_platform, BrowserTarget, Location, DetailsHash, ShortDetails], function=([count(aid, distinct=true, as=UniqueEndpoints), count(aid, as=ExecutionCount), selectFromMax(field="@timestamp", include=[aid, falconPID])]))

// Set threshold to look for results that have occurred on fewer than 50 unique endpoints; adjust up or down as desired
| test(UniqueEndpoints<50)

// Add link to Graph Explorer
| format("[Last Execution](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "falconPID"], as="Graph Explorer")

// Drop unneeded fields
| drop([aid, DetailsHash, falconPID])
```

## Query 8
```cql
```Get events of interest for T1217```
event_simpleName IN (ProcessRollup2, CommandHistory, ScriptControl*) "chrome"

```Normalize details field``` 
| eval Details=coalesce(CommandLine, CommandHistory,ScriptContent)

```Further narrow events with brute force search against Details field``` 
| search Details="*chrome*"

```Normalize Falcon UPID value``` 
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal) 

```Check to see which operating system Chrome is being targeted```
| eval BrowserTarget=case(match(Details,"(?i).*\\\\AppData\\\\Local\\\\Google\\\\Chrome\\\\User\sData\\\\Default.*"), "Windows - Google Chrome", match(Details,"(?i).*\/Users\/.+\/Library\/Application\sSupport\/Google\/Chrome\/Default.*"), "macOS - Google Chrome", match(Details,"(?i).*\/home\/.+\/\.config\/google\-chrome\/Default.*"), "Linux - Google Chrome")

```Check to see where targeting is found```
| eval Location=case(match(event_simpleName,"ProcessRollup2"), "Process Execution - Command Line", match(event_simpleName,"CommandHistory"), "Process Execution - Command History", match(event_simpleName,"^ScriptControl.*"), "Script - Script Contents")

```Created shortened Details field of 100 characters to improve readability```
| eval ShortDetails=substr(Details,1,100)

```Aggregate results```
| stats dc(aid) as UniqueEndpoints, count(aid) as ExecutionCount, last(aid) as aid, last(falconPID) as falconPID by event_platform, BrowserTarget, Location, ShortDetails

```Set threshold to look for results that have occurred on fewer than 50 unique endpoints; adjust up or down as desired```
| where UniqueEndpoints < 50

```Add link to Graph Explorer```
| eval LastExecution=case(falconPID!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . falconPID) 

```Output to table```
| table event_platform, BrowserTarget, Location, ShortDetails, UniqueEndpoints, ExecutionCount, LastExecution
```
