---
title: "ATT&CK Edition: T1580"
date: 2023-12-08
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/18dnavb/20231208_cool_query_friday_attck_edition_t1580/"
mitre: [T1010, T1087, T1087.001, T1087.002, T1087.003, T1087.004, T1217, T1580]
series: Cool Query Friday
---

# ATT&CK Edition: T1580

> Source: [https://www.reddit.com/r/crowdstrike/comments/18dnavb/20231208_cool_query_friday_attck_edition_t1580/](https://www.reddit.com/r/crowdstrike/comments/18dnavb/20231208_cool_query_friday_attck_edition_t1580/) — by Andrew-CS (CrowdStrike) — 2023-12-08

Welcome to our seventieth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval Cloud=case(match(Details,"(?i).*(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances).*"), "AWS", match(Details,"(?i).*gcloud\s+.*"), "GCP", match(Details,"(?i)az\s+.*"), "Azure")
```

## Query 2
```cql
| eval CommandDetails=substr(Details,1,200)
```

## Query 3
```cql
| rex field=Details ".*(?<Command>(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances|gcloud\s+|az\s+).*)"
```

## Query 4
```cql
| stats values(Command) as Command, values(CommandDetails) as CommandDetails, dc(aid) as UniqueEndpoints, count(aid) as ExecutionCount, last(aid) as aid, last(falconPID) as falconPID by Details, Cloud, event_simpleName
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
// Get events of interest for T1580
(#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances)/i) OR (#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(gcloud\s+compute\s+instances\s+list)/i) OR (#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(az\s+vm\s+list)/i)

// Normalize details field
| Details:=concat([CommandLine, CommandHistory,ScriptContent])

// Created shortened Details field of 100 characters to improve readability
| CommandDetails:=format("%,.200s", field=Details)

// Normalize Falcon UPID value
| falconPID:=TargetProcessId | falconPID:=ContextProcessId

// Check cloud provider
| case {
    Details=/(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances)/i | Cloud:="AWS";
    Details=/gcloud\s+/i | Cloud:="GCP";
    Details=/az\s+/i | Cloud:="Azure";
}

// Get API or command line program
| regex("(?<Command>(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances|gcloud\s+|az\s+))", field=Details, strict=false)

// Organize output
| groupBy([Details, Cloud, #event_simpleName], function=([collect([Command, CommandDetails]), count(aid, distinct=true, as=UniqueEndpoints), count(aid, as=ExecutionCount), selectFromMax(field="@timestamp", include=[aid, falconPID])]))

// Set threshold
| test(ExecutionCount<10)

// Dispaly link for Graph Explorer for last execution
| format("[Last Execution](https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:%s:%s)", field=["aid", "falconPID"], as="Graph Explorer")

// Drop unneeded fields
| drop([Details, aid, falconPID])
```

## Query 8
```cql
```Get events of interest for T1580```
(event_simpleName IN (ProcessRollup2,CommandHistory,ScriptControl*) AND ("DescribeInstances" OR "ListBuckets" OR "HeadBucket" OR "GetPublicAccessBlock" OR "DescribeDBInstances")) OR (event_simpleName IN (ProcessRollup2,CommandHistory,ScriptControl*) ("gcloud" AND "instances" AND "list")) OR (event_simpleName IN (ProcessRollup2,CommandHistory,ScriptControl*) ("az" AND "vm" AND "list"))

```Normalize details field``` 
| eval Details=coalesce(CommandLine, CommandHistory,ScriptContent)

```Normalize Falcon UPID value``` 
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal) 

```Check cloud provider```
| eval Cloud=case(match(Details,"(?i).*(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances).*"), "AWS", match(Details,"(?i).*gcloud\s+.*"), "GCP", match(Details,"(?i)az\s+.*"), "Azure")

```Created shortened Details field of 200 characters to improve readability```
| eval CommandDetails=substr(Details,1,200)

```Get command or API used```
| rex field=Details ".*(?<Command>(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances|gcloud\s+|az\s+).*)"

```Aggregate results```
| stats values(Command) as Command, values(CommandDetails) as CommandDetails, dc(aid) as UniqueEndpoints, count(aid) as ExecutionCount, last(aid) as aid, last(falconPID) as falconPID by Details, Cloud, event_simpleName

```Set threshold to look for results that have occurred on fewer than 50 unique endpoints; adjust up or down as desired```
| where UniqueEndpoints < 50

```Add link to Graph Explorer```
| eval LastExecution=case(falconPID!="","https://falcon.crowdstrike.com/graphs/process-explorer/graph?id=pid:" .aid. ":" . falconPID) 

``` Organize output to table```
|  table Cloud, event_simpleName, Command, CommandDetails, UniqueEndpoints, ExecutionCount, LastExecution
```
