---
title: "Part II: Hunting Windows RMM Tools, Custom IOAs, and SOAR Response"
date: 2024-10-24
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1gb30r9/20241024_cool_query_friday_part_ii_hunting/"
mitre: []
series: Cool Query Friday
---

# Part II: Hunting Windows RMM Tools, Custom IOAs, and SOAR Response

> Source: [https://www.reddit.com/r/crowdstrike/comments/1gb30r9/20241024_cool_query_friday_part_ii_hunting/](https://www.reddit.com/r/crowdstrike/comments/1gb30r9/20241024_cool_query_friday_part_ii_hunting/) — by Andrew-CS (CrowdStrike) — 2024-10-24

Welcome to our eighty-first installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Get all Windows process execution events
| #event_simpleName=ProcessRollup2 event_platform=Win

// Check to see if FileName value matches the value or a known RMM tools as specified by our lookup file
| match(file="rmm_list.csv", field=[FileName], column=rmm_binary, ignoreCase=true)

// Do some light formatting
| regex("(?<short_binary_name>\w+)\.exe", field=FileName)
| short_binary_name:=lower("short_binary_name")
| rmm_binary:=lower(rmm_binary)

// Aggregate by RMM program name
| groupBy([rmm_program], function=([
    collect([rmm_binary]), 
    collect([short_binary_name], separator="|"),  
    count(FileName, distinct=true, as=FileCount), 
    count(aid, distinct=true, as=EndpointCount), 
    count(aid, as=ExecutionCount)
]))

// Create case statement to display what Custom IOA regex will look like
| case{
    FileCount>1 | ImageFileName_Regex:=format(format=".*\\\\(%s)\\.exe", field=[short_binary_name]);
    FileCount=1 | ImageFileName_Regex:=format(format=".*\\\\%s\\.exe", field=[short_binary_name]);
}

// More formatting
| description:=format(format="Unexpected use of %s observed. Please investigate.", field=[rmm_program])
| rename([[rmm_program,RuleName],[rmm_binary,BinaryCoverage]])
| table([RuleName, EndpointCount, ExecutionCount, description, ImageFileName_Regex, BinaryCoverage], sortby=ExecutionCount, order=desc)
```

## Query 2
```cql
| readFile("rmm_list.csv")
| regex("(?<short_binary_name>\w+)\.exe", field=rmm_binary)
| short_binary_name:=lower("short_binary_name")
| rmm_binary:=lower(rmm_binary)
| groupBy([rmm_program], function=([
    collect([rmm_binary], separator=", "), 
    collect([short_binary_name], separator="|"), 
    count(rmm_binary, as=FileCount)
]))
| case{
    FileCount>1 | ImageFileName_Regex:=format(format=".*\\\\(%s)\\.exe", field=[short_binary_name]);
    FileCount=1 | ImageFileName_Regex:=format(format=".*\\\\%s\\.exe", field=[short_binary_name]);
}
| pattern_severity:=informational
| enabled:=false
| disposition_id:=20
| description:=format(format="Unexpected use of %s observed. Please investigate.", field=[rmm_program])
| rename([[rmm_program,RuleName],[rmm_binary,BinaryCoverage]])
| table([RuleName, pattern_severity, enabled, description, disposition_id, ImageFileName_Regex, BinaryCoverage])
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> If you have any issues during the import of `RmmToolsIoaGroup.zip`, make sure your API client has the proper permissions and that you're using the latest version of PSFalcon. You can uninstall old versions and install the latest by running these commands (assuming you used the PowerShell Gallery): Uninstall-Module -Name PSFalcon -AllVersions Install-Module -Name PSFalcon
— [CS] bk-CS · score 6

### Q&A

**Q — [Community] Dtektion_:** How can we get these IOAs if our ORG does not create APIs for users?

**A — [CS] Andrew-CS:** You could also just run the second query above as that shows the regex syntax... but if you can't create API keys I don't think you can create Custom IOA Rules either. You need to have the user permission to do one or the other.
