---
title: "correlate()"
date: 2026-03-11
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1rquf4q/20260311_cool_query_friday_correlate/"
mitre: []
series: Cool Query Friday
---

# correlate()

> Source: [https://www.reddit.com/r/crowdstrike/comments/1rquf4q/20260311_cool_query_friday_correlate/](https://www.reddit.com/r/crowdstrike/comments/1rquf4q/20260311_cool_query_friday_correlate/) — by Andrew-CS (CrowdStrike) — 2026-03-11

Welcome to our eighty-seventh installment of Cool Query Friday (on a Wednesday). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
correlate(

 // First Search
 name1: {
 YOUR SEARCH HERE
 } include: [Fields, To, Pass, To, Next, Search],

 // Second Search
 name2: {
 YOUR SEARCH HERE
 | correlationKey <=> name1.CorrelationKey
 } include: [Fields, To, Pass, To, Next, Search],

 // Search for systeminfo executions on Windows
 search3: {
 YOUR SEARCH HERE
 | correlationKey <=> name2.CorrelationKey
 } include: [Fields, To, Pass, To, Next, Search],
 
// Parameters here
sequence=false, within=5m)
```

## Query 2
```cql
correlate(

 // Search for whoami executions on Windows
 whoami: {
 #event_simpleName=ProcessRollup2 event_platform=Win FileName="whoami.exe"
 } include: [aid, ComputerName, FileName],

 // Search for net executions on Windows
 net: {
 #event_simpleName=ProcessRollup2 event_platform=Win FileName=/^net1?.exe$/
 // Correlation key between whoami search and net search
 | aid <=> whoami.aid
 } include: [aid, ComputerName, FileName],

 // Search for systeminfo executions on Windows
 systeminfo: {
 #event_simpleName=ProcessRollup2 event_platform=Win FileName="systeminfo.exe"
// Correlation key between net search and systeminfo search
 | aid <=> net.aid
 } include: [aid, ComputerName, FileName],

 sequence=false, within=5m)
```

## Query 3
```cql
[...]
| table([whoami.ComputerName, whoami.FileName, net.ComputerName, net.FileName, systeminfo.ComputerName, systeminfo.FileName])
```

## Query 4
```cql
correlate(
    // Have any event from Zscaler
    zscaler: {
         #Vendor=zscaler 
    } include: [@rawstring, user.email, client.ip],
   // Event from Okta has email that matches email from Zscaler event
    okta: {
         #Vendor=okta
        | user.name<=>zscaler.user.email
          } include: [@rawstring, user.email, client.ip],
  // Have Falcon event where external IP of endpoint matches Client IP of Zscaler event
    falcon: {
         #Vendor=crowdstrike
        | aip<=>zscaler.client.ip
          } include: [@rawstring, ComputerName, aip],
sequence=false, within=60m)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
correlate(
    // Search for grandparent process
    grandparent: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName!="explorer.exe" CommandLine=*
    } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for parent process
    parent: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="cmd.exe" CommandLine=*
          | aid <=>grandparent.aid
          | ParentProcessId<=>grandparent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine],
    // Search for child process
    child: {
         #event_simpleName=ProcessRollup2 event_platform=Win FileName="powershell.exe" CommandLine=/\-(e(nc|ncodedcommand|ncoded)?)\s+(?<ecodedBlob>\S+)/iF
            // Decoding base64
            | base64Decode("child.ecodedBlob", as=decodedBlob, charset="UTF-16LE")
          | aid<=>parent.aid
          | ParentProcessId<=>parent.TargetProcessId
          } include: [cid, aid, TargetProcessId, ParentProcessId, UserName,ComputerName, FileName, CommandLine, ecodedBlob, decodedBlob],
sequence=true, within=10m)

//  Create ProcessTree
| ProcessLineage:=format(format="%s (%s)\n\t└ %s (%s)\n\t\t└ %s (%s)", field=[grandparent.FileName, grandparent.CommandLine, parent.FileName, parent.CommandLine, child.FileName, child.CommandLine])

// Create Link to Process Explorer
| format("[Graph Explorer](/graphs/process-explorer/tree?id=pid:%s:%s&investigate=true&_cid=%s)", field=["child.aid", "child.TargetProcessId", "child.cid"], as="Graph Explorer")
```
— [CS] Andrew-CS · comment score 3

### Q&A

**Q — [Community] yankeesfan01x:** Amazing stuff, as always Andrew and CQF crew. Out of curiosity, are there some chains that you guys have seen recently in the wild that a SOC would want to key in on more than others?

**A — [CS] Andrew-CS:** I like this one that is only Falcon data, but does process chaining... correlate( // Search for grandparent process grandparent: { #event_simpleName=ProcessRollup2 event_platform=Win FileName!="explorer.exe" CommandLine=* } include: [cid, aid, TargetProcessId, ParentProcessId, UserName, ComputerName, FileName, CommandLine], // Search for parent process parent: { #event_simpleName=ProcessRollup2 event_platform=Win FileName="cmd.exe" CommandLine=* | aid <=>grandparent.aid | ParentProcessId<=>grand …
