---
title: "New Regex Engine Edition"
date: 2024-10-11
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1g1hw21/20241011_cool_query_friday_new_regex_engine/"
mitre: []
series: Cool Query Friday
---

# New Regex Engine Edition

> Source: [https://www.reddit.com/r/crowdstrike/comments/1g1hw21/20241011_cool_query_friday_new_regex_engine/](https://www.reddit.com/r/crowdstrike/comments/1g1hw21/20241011_cool_query_friday_new_regex_engine/) — by Andrew-CS (CrowdStrike) — 2024-10-11

Welcome to our seventy-ninth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| regex("foo", field=myField, flags=i, strict=true)
```

## Query 2
```cql
| myField=/foo/i
```

## Query 3
```cql
| CommandLine=/ENCRYPTED/
```

## Query 4
```cql
| CommandLine=/ENCRYPTED/i
```

## Query 5
```cql
------------------------------------------------------------------------------------
Regex \ Engine                          |  Old Eng |     Java |     New Engine 
------------------------------------------------------------------------------------
Twain                                   |   257 ms |    61.7% |    50.7% 
(?i)Twain                               |   645 ms |    83.2% |    83.7% 
[a-z]shing                              |   780 ms |   139.6% |    15.6% 
Huck[a-zA-Z]+|Saw[a-zA-Z]+              |   794 ms |   108.9% |    24.5% 
[a-q][^u-z]{13}x                        |  2378 ms |    79.0% |    46.7% 
Tom|Sawyer|Huckleberry|Finn             |   984 ms |   139.5% |    31.5% 
(?i)(Tom|Sawyer|Huckleberry|Finn)       |  1408 ms |   172.0% |    89.0% 
.{0,2}(?:Tom|Sawyer|Huckleberry|Finn)   |  2935 ms |   271.9% |    66.6% 
.{2,4}(Tom|Sawyer|Huckleberry|Finn)     |  5190 ms |   162.2% |    51.9% 
Tom.{10,25}river|river.{10,25}Tom       |   972 ms |    70.0% |    20.9% 
\s[a-zA-Z]{0,12}ing\s                   |  1328 ms |   150.2% |    58.0% 
([A-Za-z]awyer|[A-Za-z]inn)\s           |  1679 ms |   155.5% |    13.8% 
["'][^"']{0,30}[?!\.]["']               |   753 ms |    77.3% |    39.4% 
------------------------------------------------------------------------------------
```

## Query 6
```cql
| myField=/foo/iF
```

## Query 7
```cql
| regex("foo", field=myField, flags=iF, strict=true)
```

## Query 8
```cql
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName = /\\powershell(_ise)?\.exe/i
| CommandLine=/\s-[e^]{1,2}[ncodema^]+\s(?<base64string>\S+)/i
```
