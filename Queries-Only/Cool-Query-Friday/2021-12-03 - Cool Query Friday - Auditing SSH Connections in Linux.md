---
title: "Auditing SSH Connections in Linux"
date: 2021-12-03
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/r80usb/20211203_cool_query_friday_auditing_ssh/"
mitre: []
series: Cool Query Friday
---

# Auditing SSH Connections in Linux

> Source: [https://www.reddit.com/r/crowdstrike/comments/r80usb/20211203_cool_query_friday_auditing_ssh/](https://www.reddit.com/r/crowdstrike/comments/r80usb/20211203_cool_query_friday_auditing_ssh/) — by Andrew-CS (CrowdStrike) — 2021-12-03

Welcome to our thirty-first installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| eventstats list(EnvironmentVariableName) as EnvironmentVariableName,list(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal
```

## Query 2
```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| eventstats list(EnvironmentVariableName) as EnvironmentVariableName,list(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal
| eval tempData=mvzip(EnvironmentVariableName,EnvironmentVariableValue,":")
```

## Query 3
```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| eventstats list(EnvironmentVariableName) as EnvironmentVariableName,list(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal
| eval tempData=mvzip(EnvironmentVariableName,EnvironmentVariableValue,":") 
| table ComputerName tempData
```

## Query 4
```cql
[...]
| rex field=tempData "SSH_CONNECTION\:((?<clientIP>\d+\.\d+\.\d+\.\d+)\s+(?<rPort>\d+)\s+(?<serverIP>\d+\.\d+\.\d+\.\d+)\s+(?<lPort>\d+))"
| rex field=tempData "USER\:(?<userName>.*)"
```

## Query 5
```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| eventstats list(EnvironmentVariableName) as EnvironmentVariableName,list(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal
| eval tempData=mvzip(EnvironmentVariableName,EnvironmentVariableValue,":")
| rex field=tempData "SSH_CONNECTION\:((?<clientIP>\d+\.\d+\.\d+\.\d+)\s+(?<rPort>\d+)\s+(?<serverIP>\d+\.\d+\.\d+\.\d+)\s+(?<lPort>\d+))"
| rex field=tempData "USER\:(?<userName>.*)"
| where isnotnull(clientIP)
| table ComputerName userName serverIP lPort clientIP rPort
```

## Query 6
```cql
[...]
| iplocation clientIP
| lookup local=true aid_master aid OUTPUT Version as osVersion, Country as sshServerCountry
| fillnull City, Country, Region value="-"
```

## Query 7
```cql
[...]
| table _time aid ComputerName sshServerCountry osVersion serverIP lPort userName clientIP rPort City Region Country
| where isnotnull(userName)
| sort +ComputerName, +_time
```

## Query 8
```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| eventstats list(EnvironmentVariableName) as EnvironmentVariableName,list(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal
| eval tempData=mvzip(EnvironmentVariableName,EnvironmentVariableValue,":")
| rex field=tempData "SSH_CONNECTION\:((?<clientIP>\d+\.\d+\.\d+\.\d+)\s+(?<rPort>\d+)\s+(?<serverIP>\d+\.\d+\.\d+\.\d+)\s+(?<lPort>\d+))"
| rex field=tempData "USER\:(?<userName>.*)"
| where isnotnull(clientIP)
| iplocation clientIP
| lookup local=true aid_master aid OUTPUT Version as osVersion, Country as sshServerCountry
| fillnull City, Country, Region value="-"
| table _time aid ComputerName sshServerCountry osVersion serverIP lPort userName clientIP rPort City Region Country
| where isnotnull(userName)
| sort +ComputerName, +_time
```

## Query 9
```cql
[...]
| search NOT Country IN ("-", "United States")
```

## Query 10
```cql
[...]
| search userName=root
```

## Query 11
```cql
[...]
| search NOT clientIP IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
event_platfrom=lin event_simpleName=ProcessRollup2 FileName IN (scp, sftp)
| table _time ComputerName FileName CommandLine
```
— [CS] Andrew-CS · comment score 1

```cql
event_platform=lin event_simpleName=CriticalEnvironmentVariableChanged, EnvironmentVariableName IN (SSH_CONNECTION, USER) 
| stats values(EnvironmentVariableName) as EnvironmentVariableName,values(EnvironmentVariableValue) as EnvironmentVariableValue by aid, ContextProcessId_decimal, ContextTimeStamp_decimal
| eval tempData=mvzip(EnvironmentVariableName,EnvironmentVariableValue,":")
| rex field=tempData "SSH_CONNECTION\:((?<clientIP>\d+\.\d+\.\d+\.\d+)\s+(?<rPort>\d+)\s+(?<serverIP>\d+\.\d+\.\d+\.\d+)\s+(?<lPort>\d+))"
| rex field=tempData "USER\:(?<userName>.*)"
| where isnotnull(clientIP)
| iplocation clientIP
| lookup local=true aid_master aid OUTPUT ComputerName as ComputerName, Version as osVersion, Country as sshServerCountry
| fillnull City, Country, Region value="-"
| table ContextTimeStamp_decimal aid ComputerName sshServerCountry osVersion serverIP lPort userName clientIP rPort City Region Country
| where isnotnull(userName)
| convert ctime(ContextTimeStamp_decimal)
| sort +ComputerName, +ContextTimeStamp_decimal
```
— [CS] Andrew-CS · comment score 3

```cql
cat /var/log/auth.log | grep "Failed password"
```
— [CS] Andrew-CS · comment score 2

### Operational caveats

> Hi there. If you specify the `index` and `sourcetype` you're using in your Splunk instance does performance improve?
— [CS] Andrew-CS · score 2

### Q&A

**Q — [Community] brandeded:** How can scp usage and sftp subsystem usage be identified?

**A — [CS] Andrew-CS:** Hi there. Since those are both programs, you would look for `ProcessRollup2` events. event_platfrom=lin event_simpleName=ProcessRollup2 FileName IN (scp, sftp) | table _time ComputerName FileName CommandLine That will show you those events.

**Q — [Community] brandeded:** Meaning, if I run 'pscp' on my Windows client, it invokes `scp` on the server?

**A — [CS] Andrew-CS:** If Falcon is on both systems, you should see a `ProcessRollup2` event for `pscp` on your Windows system and an SSH Login on the server system assuming the server is Linux.

**Q — [Community] brandeded:** Yes. To confirm, this means that `scp` usage can't be observed server side with crowdstrike, but could be observed on-the-wire. Crowdstrike can not observe packets inbound?

**A — [CS] Andrew-CS:** Correct, because from a process execution standpoint scp isn't running on the server. If you were to have SSL interception/inspection you might be able to determine SCP, but again on the surface it will look like SSH from the packet generics.
