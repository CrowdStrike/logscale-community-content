---
title: "Hunting Windows RMM Tools"
date: 2024-10-18
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1g6iupi/20241018_cool_query_friday_hunting_windows_rmm/"
mitre: []
series: Cool Query Friday
---

# Hunting Windows RMM Tools

> Source: [https://www.reddit.com/r/crowdstrike/comments/1g6iupi/20241018_cool_query_friday_hunting_windows_rmm/](https://www.reddit.com/r/crowdstrike/comments/1g6iupi/20241018_cool_query_friday_hunting_windows_rmm/) — by Andrew-CS (CrowdStrike) — 2024-10-18

Welcome to our eightieth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
grep -ERi "\-\s\w+\.exe" . | awk -F\- '{ print $2 }' | sed "s/^[ \t]*//" | awk '{print tolower($0)}' | sort -u
```

## Query 2
```cql
// Get all Windows Process Executions
#event_simpleName=ProcessRollup2 event_platform=Win

// Check to see if FileName matches our list of RMM tools
| match(file="rmm_executables_list.csv", field=[FileName], column=rmm, ignoreCase=true)

// Create short file path field
| FilePath=/\\Device\\HarddiskVolume\d+(?<ShortPath>.+$)/

// Aggregate results by FileName
| groupBy([FileName], function=([count(), count(aid, distinct=true, as=UniqueEndpoints), collect([ShortPath])]))

// Sort in descending order so most prevalent binaries appear first
| sort(_count, order=desc, limit=5000)
```

## Query 3
```cql
// Get all Windows Process Executions
#event_simpleName=ProcessRollup2 event_platform=Win

// Create exclusions for approved filenames
| !in(field="FileName", values=[mstsc.exe], ignoreCase=true)

// Check to see if FileName matches our list of RMM tools
| match(file="rmm_executables_list.csv", field=[FileName], column=rmm, ignoreCase=true)
```

## Query 4
```cql
// Get all Windows Process Executions
#event_simpleName=ProcessRollup2 event_platform=Win

// Create exclusions for approved filenames
| !in(field="FileName", values=[mstsc.exe], ignoreCase=true)

// Check to see if FileName matches our list of RMM tools
| match(file="rmm_executables_list.csv", field=[FileName], column=rmm, ignoreCase=true)

// Create pretty ExecutionChain field
| ExecutionChain:=format(format="%s\n\t└ %s (%s)", field=[ParentBaseFileName, FileName, RawProcessId])

// Perform aggregation
| groupBy([@timestamp, aid, ComputerName, UserName, ExecutionChain, CommandLine, TargetProcessId, SHA256HashData], function=[], limit=max)

// Create link to VirusTotal to search SHA256
| format("[Virus Total](https://www.virustotal.com/gui/file/%s)", field=[SHA256HashData], as="VT")

// SET FLACON CLOUD; ADJUST COMMENTS TO YOUR CLOUD
| rootURL := "https://falcon.crowdstrike.com/" /* US-1*/
//rootURL  := "https://falcon.eu-1.crowdstrike.com/" ; /*EU-1 */
//rootURL  := "https://falcon.us-2.crowdstrike.com/" ; /*US-2 */
//rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" ; /*GOV-1 */

// Create link to Indicator Graph for easier scoping by SHA256
| format("[Indicator Graph](%sintelligence/graph?indicators=hash:'%s')", field=["rootURL", "SHA256HashData"], as="Indicator Graph")

// Create link to Graph Explorer for process specific investigation
| format("[Graph Explorer](%sgraphs/process-explorer/graph?id=pid:%s:%s)", field=["rootURL", "aid", "TargetProcessId"], as="Graph Explorer")

// Drop unneeded fields
| drop([SHA256HashData, TargetProcessId, rootURL])
```

## Query 5
```cql
// Create exclusions for approved users
| !in(field="UserName", values=[Admin, Administrator, Bob, Alice], ignoreCase=true)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| readFile("rmm_list.csv")
| regex("(?<short_binary_name>\w+)\.exe", field=rmm_binary)
| groupBy([rmm_program], function=([collect([rmm_binary]), collect([short_binary_name], separator="|"), count(rmm_binary, as=FileCount)]))
| short_binary_name:=lower("short_binary_name")
| case{
    FileCount>1 | IOAruleRegex:=format(format="\\\\(%s)\\.exe", field=[short_binary_name]);
    FileCount=1 | IOAruleRegex:=format(format="\\\\%s\\.exe", field=[short_binary_name]);
}
| drop([short_binary_name])
| rename(field="rmm_binary", as="Binary_Coverage")
| rename(field="rmm_program", as="Program_Name")
| table([Program_Name, IOAruleRegex, Binary_Coverage])
```
— [CS] Andrew-CS · comment score 2

### Operational caveats

> Hi there. This is more of an application control use-case. You can use a Custom IOA to block the process names, but I would break that up into a rule for each program so you can tweak and tune as necessary.
— [CS] Andrew-CS · score 1

> Hi there. The attached RMM CSV file has been updated on GitHub. If you downloaded before 2024-10-22 @ 0800 EST, please redownload and replace the version you are using. There were some parsing errors so "teamviewer.exe" was showing up as "eamviewer.exe". Fixed now!
— [CS] Andrew-CS · score 5

### Q&A

**Q — [Community] red_devillzz:** Can you help on how we can block execution of so many executable at scale in a corporate environment. Is there a way to do this in Crowdstrike?

**A — [CS] Andrew-CS:** Hi there. This is more of an application control use-case. You can use a Custom IOA to block the process names, but I would break that up into a rule for each program so you can tweak and tune as necessary.
