---
title: "Hunting Fake CAPTCHA Artifacts in Windows"
date: 2025-04-14
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1jz02j3/20250414_cool_query_friday_hunting_fake_captcha/"
mitre: []
series: Cool Query Friday
---

# Hunting Fake CAPTCHA Artifacts in Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/1jz02j3/20250414_cool_query_friday_hunting_fake_captcha/](https://www.reddit.com/r/crowdstrike/comments/1jz02j3/20250414_cool_query_friday_hunting_fake_captcha/) — by Andrew-CS (CrowdStrike) — 2025-04-14

Welcome to our eighty-fourth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/?f=flair_name%3A%22CQF%22) (on a Monday). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
Get-ChildItem "Registry::HKEY_USERS" | 
    ForEach-Object {
        $SID = $_.PSChildName
        $RunMRUPath = "Registry::HKEY_USERS\$SID\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
        
        if (Test-Path $RunMRUPath) {
            # Try to get username from SID
            try {
                $UserName = (New-Object System.Security.Principal.SecurityIdentifier($SID)).Translate([System.Security.Principal.NTAccount]).Value
            }
            catch {
                $UserName = $SID  # Keep SID if translation fails
            }
            
            $RunMRUValues = Get-ItemProperty -Path $RunMRUPath
            $RunMRUValues.PSObject.Properties | 
                Where-Object { $_.Name -match '^[a-z]$' } | 
                ForEach-Object { Write-Output "$UserName : $($_.Name): $($_.Value)" }
        }
    }
```

## Query 2
```cql
#event_simpleName=ProcessRollup2 AND WindowFlags=1025 AND LinkName!="*" ParentBaseFileName=explorer.exe ImageSubsystem=3
| CmdLength:=length("CommandLine")
// Can raise or loweer this threshold
| test(CmdLength>100)
// Checks for presense of "http" or "https"
| CommandLine=/https?/iF
| table([@timestamp, aid, ComputerName, UserName, UserSid, FileName, CmdLength, CommandLine], sortby=CmdLength, order=desc, limit=500)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> Hey there. Interrogating and clouding the contents of the call stack for every execution has a negative impact on system performance. That's why it isn't everywhere. Just so you know :) I'll get with research and see if there have been any movements, here.
— [CS] Andrew-CS · score 2
