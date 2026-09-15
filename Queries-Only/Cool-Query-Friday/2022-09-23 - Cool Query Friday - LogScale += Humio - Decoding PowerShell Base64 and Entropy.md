---
title: "LogScale += Humio - Decoding PowerShell Base64 and Entropy"
date: 2022-09-23
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/xm7lsn/20220923_cool_query_friday_logscale_humio/"
mitre: []
series: Cool Query Friday
---

# LogScale += Humio - Decoding PowerShell Base64 and Entropy

> Source: [https://www.reddit.com/r/crowdstrike/comments/xm7lsn/20220923_cool_query_friday_logscale_humio/](https://www.reddit.com/r/crowdstrike/comments/xm7lsn/20220923_cool_query_friday_logscale_humio/) — by Andrew-CS (CrowdStrike) — 2022-09-23

Welcome to our fiftieth (50, baby!) installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
//Look for command line flags that indicate an encoded command
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+/i
```

## Query 2
```cql
//Group by command frequency
| groupby([ParentBaseFileName, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
```

## Query 3
```cql
//Grab all PowerShell execution events
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\powershell(_ise)?\.exe/i
//Look for command line flags that indicate an encoded command
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+/i
//Group by command frequency
| groupby([ParentBaseFileName, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
//Organizing fields
| table([uniqueEndpointCount, executionCount, ParentBaseFileName, CommandLine])
//Sorting by unique endpoints
| sort(field=uniqueEndpointCount, order=desc)
```

## Query 4
```cql
//Setting prevalence threshold
| uniqueEndpointCount < 3
```

## Query 5
```cql
//Calculating the length of the encrypted command line
| cmdLength := length("CommandLine")
```

## Query 6
```cql
//Isolate Base64 String
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+(?<base64String>\S+)/i
```

## Query 7
```cql
//Get Entropy of Base64 String
| b64Entroy := shannonEntropy("base64String")
```

## Query 8
```cql
//Setting entropy threshold
| b64Entroy > 3.5
```

## Query 9
```cql
//Decode encoded command blob
| decodedCommand := base64Decode(base64String, charset="UTF-16LE")
```

## Query 10
```cql
//Grab all PowerShell execution events
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\powershell(_ise)?\.exe/i
//Look for command line flags that indicate an encoded command
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+/i
//Group by command frequency
| groupby([ParentBaseFileName, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
//Setting prevalence threshold
| uniqueEndpointCount < 3
//Calculating the length of the encrypted command line
| cmdLength := length("CommandLine")
//Isolate Base64 String
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+(?<base64String>\S+)/i
//Get Entropy of Base64 String
| b64Entroy := shannonEntropy("base64String")
//Decode encoded command blob
| decodedCommand := base64Decode(base64String, charset="UTF-16LE")
| table([ParentBaseFileName, uniqueEndpointCount, executionCount, cmdLength,  b64Entroy, decodedCommand])
```

## Query 11
```cql
//Search for http or https in command line
| decodedCommand=/https?/i
```

## Query 12
```cql
//Grab all PowerShell execution events
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\powershell(_ise)?\.exe/i
//Look for command line flags that indicate an encoded command
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+/i
//Group by command frequency
| groupby([ParentBaseFileName, CommandLine], function=stats([count(aid, distinct=true, as="uniqueEndpointCount"), count(aid, as="executionCount")]), limit=max)
//Setting prevalence threshold
| uniqueEndpointCount < 3
//Calculating the length of the encrypted command line
| cmdLength := length("CommandLine")
//Isolate Base64 String
| CommandLine=/\s+\-(e\s|enc|encodedcommand|encode)\s+(?<base64String>\S+)/i
//Get Entropy of Base64 String
| b64Entroy := shannonEntropy("base64String")
//Setting entropy threshold
| b64Entroy > 3.5
//Decode encoded command blob
| decodedCommand := base64Decode(base64String, charset="UTF-16LE")
//Outputting to table
| table([ParentBaseFileName, uniqueEndpointCount, executionCount, cmdLength,  b64Entroy, decodedCommand])
//Search for http or https in command line
| decodedCommand=/https?/i
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> Splunk was never “the back end”, that’s Threat, Intel or Asset Graph depending on module. What you’re seeing in the GUI is a highly customized version of the Splunk UI that can access this data and facilitates capabilities for raw searching. I’m not going to spoil our future but we have big things planned, be sure to attend the quarterly roadmap calls for more information!
— [CS] BradW-CS · score 3
