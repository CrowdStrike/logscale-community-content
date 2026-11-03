---
title: "ATT&CK Edition: T1087.003"
date: 2023-10-20
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/17c9nel/20231020_cool_query_friday_attck_edition_t1087003/"
mitre: [T1087, T1087.002, T1087.003]
series: Cool Query Friday
---

# ATT&CK Edition: T1087.003

> Source: [https://www.reddit.com/r/crowdstrike/comments/17c9nel/20231020_cool_query_friday_attck_edition_t1087003/](https://www.reddit.com/r/crowdstrike/comments/17c9nel/20231020_cool_query_friday_attck_edition_t1087003/) — by Andrew-CS (CrowdStrike) — 2023-10-20

Welcome to our sixty-sixth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval Description=case(match(CommandLine,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in command line invocation.", match(CommandHistory,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in command line history.", match(ScriptContent,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in script contents.")
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
#event_simpleName=/^(ProcessRollup2$|CommandHistory$|ScriptControl)/ event_platform=Win
```

## Query 5
```cql
#event_simpleName=/^(ProcessRollup2$|CommandHistory$|ScriptControl)/
| /(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook)/i
```

## Query 6
```cql
// Get events in scope for T1087.003
#event_simpleName=/^(ProcessRollup2$|CommandHistory$|ScriptControl)/

// Get strings of interest
| /(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook)/i

// Create "Description" field based on location of target string
| case {
   #event_simpleName=CommandHistory AND CommandHistory=/(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook)/i | Description:="T1087.003 discovered in command line history.";
   #event_simpleName=ProcessRollup2 AND CommandLine=/(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook)/i | Description:="T1087.003 discovered in command line invocation.";
   #event_simpleName=/^ScriptControl/ AND ScriptContent=/(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook)/i | Description:="T1087.003 discovered in script contents.";
   * | Description:="T1087.003 discovered in general event telemetry.";
}

// Concatenate fields of interest from events of interest
| Details:=concat([CommandHistory,CommandLine,ScriptContent])

// Format output into table
| select([@timestamp, ComputerName, aid, UserName, UserSid, TargetProcessId, Description, Details])

// Add link to Graph Explorer
| format("[Graph Explorer](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "TargetProcessId"], as="Graph Explorer")
```

## Query 7
```cql
```Get events in scope for T1087.003```
event_simpleName IN (ProcessRollup2, CommandHistory, ScriptControl*) event_platform=Win ("Get-AddressList" OR "Get-GlobalAddressList" OR "Get-OfflineAddressBook")

```Create "Description" field based on location of target string```
| eval Description=case(match(CommandLine,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in command line invocation.", match(CommandHistory,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in command line history.", match(ScriptContent,".*(Get-AddressList|Get-GlobalAddressList|Get-OfflineAddressBook).*"), "T1087.003 discovered in script contents.")

```Concat fields of interest from events of interest```
| eval Details=coalesce(CommandLine, CommandHistory, ScriptContent)

```Format output into table```
| table _time, ComputerName, aid, UserName, UserSid_readable, TargetProcessId_decimal, Description, Details

```Add link to Graph Explorer```
| eval GraphExplorer=case(TargetProcessId_decimal!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . TargetProcessId_decimal)
```
