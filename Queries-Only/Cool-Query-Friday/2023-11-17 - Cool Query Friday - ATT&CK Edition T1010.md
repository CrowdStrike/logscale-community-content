---
title: "ATT&CK Edition: T1010"
date: 2023-11-17
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/17xa6vm/20231117_cool_query_friday_attck_edition_t1010/"
mitre: [T1010, T1087, T1087.001, T1087.002, T1087.003, T1087.004]
series: Cool Query Friday
---

# ATT&CK Edition: T1010

> Source: [https://www.reddit.com/r/crowdstrike/comments/17xa6vm/20231117_cool_query_friday_attck_edition_t1010/](https://www.reddit.com/r/crowdstrike/comments/17xa6vm/20231117_cool_query_friday_attck_edition_t1010/) — by Andrew-CS (CrowdStrike) — 2023-11-17

Welcome to our sixty-eighth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval Description=case(match(event_simpleName,"ProcessRollup2"), "T1010 discovered in command line invocation.", match(event_simpleName,"CommandHistory"), "T1010 discovered in command line history.", match(event_simpleName,"ScriptControl.*"), "T1010 discovered in script contents.")
```

## Query 2
```cql
| eval Details=coalesce(CommandLine, CommandHistory, ScriptContent)
```

## Query 3
```cql
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
```

## Query 4
```cql
| table _time, ComputerName, aid, UserName, UserSid_readable, falconPID, Description, Details
```

## Query 5
```cql
// Get events of interest where enumeration APIs may be called in scope for T1010.
#event_simpleName=/^(ProcessRollup2$|CommandHistory$|ScriptControl)/ event_platform=Win /(mainWindowTitle|Get-Process|GetForegroundWindow|GetProcesses)/i

// Concatenate fields of interest from events of interest
| Details:=concat([CommandHistory,CommandLine,ScriptContent])

// Create "Description" field based on location of target string
| case {
#event_simpleName=CommandHistory | Description:="T1010 discovered in command line history.";
#event_simpleName=ProcessRollup2 | Description:="T1010 discovered in command line invocation.";
#event_simpleName=/^ScriptControl/ | Description:="T1010 discovered in script contents.";
* | Description:="T1010 discovered in general event telemetry.";
}

// Normalize UPID
| falconPID:=TargetProcessId | falconPID:=ContextProcessId

// Format output to table
| select([@timestamp, ComputerName, aid, UserName, UserSid, falconPID, Description, Details])

// Add link to Graph Explorer
| format("[Graph Explorer](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "falconPID"], as="Graph Explorer")
```

## Query 6
```cql
```Get events of interest where enumeration APIs may be called in scope for T1010```
event_simpleName IN (ProcessRollup2, CommandHistory, ScriptControl*) event_platform=Win ("mainWindowTitle" OR "Get-Process" OR "GetForegroundWindow" OR "GetProcesses")

```Create "Description" field based on location of target string```
| eval Description=case(match(event_simpleName,"ProcessRollup2"), "T1010 discovered in command line invocation.", match(event_simpleName,"CommandHistory"), "T1010 discovered in command line history.", match(event_simpleName,"ScriptControl.*"), "T1010 discovered in script contents.")

```Concat fields of interest from events of interest```
| eval Details=coalesce(CommandLine, CommandHistory, ScriptContent)

```Normalize UPID```
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)

```Format output into table```
| table _time, ComputerName, aid, UserName, UserSid_readable, falconPID, Description, Details

```Add link to Graph Explorer```
| eval GraphExplorer=case(TargetProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . falconPID)
```
