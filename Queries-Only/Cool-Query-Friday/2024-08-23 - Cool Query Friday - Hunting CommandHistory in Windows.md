---
title: "Hunting CommandHistory in Windows"
date: 2024-08-23
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1ezcbjx/20240823_cool_query_friday_hunting_commandhistory/"
mitre: []
series: Cool Query Friday
---

# Hunting CommandHistory in Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/1ezcbjx/20240823_cool_query_friday_hunting_commandhistory/](https://www.reddit.com/r/crowdstrike/comments/1ezcbjx/20240823_cool_query_friday_hunting_commandhistory/) — by Andrew-CS (CrowdStrike) — 2024-08-23

Welcome to our seventy-seventh installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get CommandHistory and ProcessRollup2 events on Windows
#event_simpleName=/^(CommandHistory|ProcessRollup2)$/ event_platform=Win
```

## Query 2
```cql
| case{
    // Check to see if event is CommandHistory
    #event_simpleName=CommandHistory
    // This is keyword list; modify as desired
    | CommandHistory=/(add|user|password|pass|stop|start)/i
    // This puts the CommandHistory entries into an array
    | CommandHistorySplit:=splitString(by="¶", field=CommandHistory)
    // This combines the array values and separates them with a new-line
    | concatArray("CommandHistorySplit", separator="\n", as=CommandHistoryClean);
    // Check to see if event is ProcessRollup2. If yes, create mini process tree
    #event_simpleName="ProcessRollup2" | ExecutionChain:=format(format="%s\n\t└ %s (%s)", field=[ParentBaseFileName, FileName, RawProcessId]);
}
```

## Query 3
```cql
// This is keyword list; modify as desired
| CommandHistory=/(add|user|pass|stop|start|sc\s+|whoami)/i
```

## Query 4
```cql
// Use selfJoinFilter to pair PR2 and CH events
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName="ProcessRollup2"}, {#event_simpleName="CommandHistory"}])
```

## Query 5
```cql
// Aggregate to display details
| groupBy([aid, TargetProcessId], function=([collect([ProcessStartTime, ComputerName, UserName, UserSid, ExecutionChain, CommandHistoryClean])]), limit=max)
```

## Query 6
```cql
// Check to make sure CommandHistoryClean is populated due to non-deterministic nature of selfJoinFilter
| CommandHistoryClean=*

// OPTIONAL: exclude UserName values of administrators that are authorized
| !in(field="UserName", values=[svc_runbook, janeHR], ignoreCase=true)

// Format ProcessStartTime to human-readable
| ProcessStartTime:=ProcessStartTime*1000 | ProcessStartTime:=formatTime(format="%F %T.%L %Z", field="ProcessStartTime")
```

## Query 7
```cql
// Get CommandHistory and ProcessRollup2 events on Windows
#event_simpleName=/^(CommandHistory|ProcessRollup2)$/ event_platform=Win

| case{
    // Check to see if event name is CommandHistory
    #event_simpleName=CommandHistory
    // This is keyword list; modify as desired
    | CommandHistory=/(add|user|password|pass|stop|start)/i
    // This puts the CommandHistory entries into an array
    | CommandHistorySplit:=splitString(by="¶", field=CommandHistory)
    // This combines the array values and separates them with a new-line
    | concatArray("CommandHistorySplit", separator="\n", as=CommandHistoryClean);
    // Check to see if event name is ProcessRollup2. If yes, create mini process tree
    #event_simpleName="ProcessRollup2" | ExecutionChain:=format(format="%s\n\t└ %s (%s)", field=[ParentBaseFileName, FileName, RawProcessId]);
}

// Use selfJoinFilter to pair PR2 and CH events
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName="ProcessRollup2"}, {#event_simpleName="CommandHistory"}])

// Aggregate to merge PR2 and CH events
| groupBy([aid, TargetProcessId], function=([collect([ProcessStartTime, ComputerName, UserName, UserSid, ExecutionChain, CommandHistoryClean])]), limit=max)

// Check to make sure CommandHistoryClean is populated due to non-deterministic nature of selfJoinFilter
| CommandHistoryClean=*

// OPTIONAL: exclude UserName values of administrators that are authorized
| !in(field="UserName", values=[userName1, userName2], ignoreCase=true)

// Format ProcessStartTime to human-readable
| ProcessStartTime:=ProcessStartTime*1000 | ProcessStartTime:=formatTime(format="%F %T.%L %Z", field="ProcessStartTime")
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
// Calculate length of CommandHistory event
| CommandLength:=length(CommandHistory) 

// Aggregate to merge PR2 and CH events
| groupBy([aid, TargetProcessId], function=([
    collect([ProcessStartTime, ComputerName, UserName, UserSid, ExecutionChain, CommandLength, CommandHistoryClean])]), limit=max)
```
— [CS] Andrew-CS · comment score 2

```cql
// Check to see if event name is CommandHistory
    #event_simpleName=CommandHistory
    // This is keyword list; modify as desired
    | CommandHistory=/(add|user|password|pass|stop|start)/i
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] LongRichardMan:** If I wanted the query to only detect if it matched ALL of the keywords or, say only if the command history has 3 of the keywords listed. Is there a way to accomplish that?

**A — [CS] Andrew-CS:** It would be pretty simple, honestly. // Get CommandHistory with keywords and ProcessRollup2 events on Windows event_platform=Win (#event_simpleName=CommandHistory CommandHistory=/word1/i CommandHistory=/word2/i CommandHistory=/word3/i) OR (#event_simpleName=ProcessRollup2) You can change the first line to that and remove the following from the case statement: // Check to see if event name is CommandHistory #event_simpleName=CommandHistory // This is keyword list; modify as desired | CommandHisto …
