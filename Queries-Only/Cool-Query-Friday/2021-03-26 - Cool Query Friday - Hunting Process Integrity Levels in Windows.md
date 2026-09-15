---
title: "Hunting Process Integrity Levels in Windows"
date: 2021-03-26
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/mdo3dx/20210326_cool_query_friday_hunting_process/"
mitre: [T0004]
series: Cool Query Friday
---

# Hunting Process Integrity Levels in Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/mdo3dx/20210326_cool_query_friday_hunting_process/](https://www.reddit.com/r/crowdstrike/comments/mdo3dx/20210326_cool_query_friday_hunting_process/) — by Andrew-CS (CrowdStrike) — 2021-03-26

Welcome to our fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
event_platform=win ComputerName=COMPUTERNAME event_simpleName=ProcessRollup2 FileName=cmd.exe 
| table _time ComputerName UserName FileName FilePath IntegrityLevel_decimal
```

## Query 2
```cql
event_platform=win ComputerName=COMPUTERNAME event_simpleName=ProcessRollup2 FileName=cmd.exe 
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
```

## Query 3
```cql
event_platform=win ComputerName=COMPUTERNAME event_simpleName=ProcessRollup2 FileName=cmd.exe 
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| table _time ComputerName UserName FileName FilePath IntegrityLevel_hex IntegrityLevel_decimal
```

## Query 4
```cql
event_platform=win ComputerName=COMPUTERNAME event_simpleName=ProcessRollup2 FileName=cmd.exe 
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| eval TokenType_decimal = replace(TokenType_decimal,"1", "PRIMARY")
| eval TokenType_decimal = replace(TokenType_decimal,"2", "IMPERSONATION")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x0000", "UNSTRUSTED")
| eval IntegrityLeve_hex = replace(IntegrityLevel_hex,"0x1000", "LOW")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2000", "MEDIUM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2100", "MEDIUM-HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x3000", "HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x4000", "SYSTEM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x5000", "PROTECTED")
| table _time ComputerName UserName FileName FilePath TokenType_decimal IntegrityLevel_hex
```

## Query 5
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 UserSid_readable=S-1-5-21-*
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| eval TokenType_decimal = replace(TokenType_decimal,"1", "PRIMARY")
| eval TokenType_decimal = replace(TokenType_decimal,"2", "IMPERSONATION")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x0000", "UNSTRUSTED")
| eval IntegrityLeve_hex = replace(IntegrityLevel_hex,"0x1000", "LOW")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2000", "MEDIUM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2100", "MEDIUM-HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x3000", "HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x4000", "SYSTEM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x5000", "PROTECTED")
| search IntegrityLevel_hex=HIGH
| stats count(aid) as executionCount dc(aid) as endpointCount dc(UserSid_readable) as userCount values(UserSid_readable) as - userSIDs by FileName FilePath TokenType_decimal IntegrityLevel_hex
| sort - executionCount
```

## Query 6
```cql
event_platform=win event_simpleName=ProcessRollup2 ImageSubsystem_decimal=3 UserSid_readable=S-1-5-21-* FileName=powershell.exe
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| eval TokenType_decimal = replace(TokenType_decimal,"1", "PRIMARY")
| eval TokenType_decimal = replace(TokenType_decimal,"2", "IMPERSONATION")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x0000", "UNSTRUSTED")
| eval IntegrityLeve_hex = replace(IntegrityLevel_hex,"0x1000", "LOW")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2000", "MEDIUM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2100", "MEDIUM-HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x3000", "HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x4000", "SYSTEM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x5000", "PROTECTED")
| search IntegrityLevel_hex=HIGH
| stats count(aid) as executionCount dc(aid) as endpointCount dc(UserSid_readable) as userCount by FileName FilePath TokenType_decimal IntegrityLevel_hex CommandLine
| sort - executionCount
```

## Query 7
```cql
event_platform=win event_simpleName=ProcessRollup2 UserSid_readable=S-1-5-21-* FilePath=*\\AppData\\*
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| eval TokenType_decimal = replace(TokenType_decimal,"1", "PRIMARY")
| eval TokenType_decimal = replace(TokenType_decimal,"2", "IMPERSONATION")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x0000", "UNSTRUSTED")
| eval IntegrityLeve_hex = replace(IntegrityLevel_hex,"0x1000", "LOW")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2000", "MEDIUM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2100", "MEDIUM-HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x3000", "HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x4000", "SYSTEM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x5000", "PROTECTED")
| search IntegrityLevel_hex=HIGH
| stats count(aid) as executionCount dc(aid) as endpointCount dc(UserSid_readable) as userCount by FileName FilePath TokenType_decimal IntegrityLevel_hex CommandLine
| sort - executionCount
```

## Query 8
```cql
event_platform=win event_simpleName=ProcessRollup2 UserSid_readable=S-1-5-21-*
| eval IntegrityLevel_hex=tostring(IntegrityLevel_decimal,"hex")
| eval TokenType_decimal = replace(TokenType_decimal,"1", "PRIMARY")
| eval TokenType_decimal = replace(TokenType_decimal,"2", "IMPERSONATION")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x0000", "UNSTRUSTED")
| eval IntegrityLeve_hex = replace(IntegrityLevel_hex,"0x1000", "LOW")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2000", "MEDIUM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x2100", "MEDIUM-HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x3000", "HIGH")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x4000", "SYSTEM")
| eval IntegrityLevel_hex = replace(IntegrityLevel_hex,"0x5000", "PROTECTED")
| search IntegrityLevel_hex=SYSTEM
| stats count(aid) as executionCount dc(aid) as endpointCount dc(UserSid_readable) as userCount by FileName FilePath TokenType_decimal IntegrityLevel_hex CommandLine
| sort - executionCount
```
