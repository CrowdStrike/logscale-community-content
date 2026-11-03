---
title: "Hunting ISO Mounts with New Telemetry"
date: 2022-07-15
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/vzosj9/20220715_cool_query_friday_hunting_iso_mounts/"
mitre: []
series: Cool Query Friday
---

# Hunting ISO Mounts with New Telemetry

> Source: [https://www.reddit.com/r/crowdstrike/comments/vzosj9/20220715_cool_query_friday_hunting_iso_mounts/](https://www.reddit.com/r/crowdstrike/comments/vzosj9/20220715_cool_query_friday_hunting_iso_mounts/) — by Andrew-CS (CrowdStrike) — 2022-07-15

Welcome to our forty-fifth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval driveType=case(VirtualDriveFileType_decimal=1, "ISO", VirtualDriveFileType_decimal=2, "VHD", VirtualDriveFileType_decimal=3, "VHDX", VirtualDriveFileType_decimal=0, "Unknown")
```

## Query 2
```cql
[...]
| rex field=VirtualDriveFileName ".*\\\(?<isoName>.*\.(img|iso))"
```

## Query 3
```cql
[...]
| table ContextTimeStamp_decimal, aid, ComputerName, VolumeDriveLetter, VolumeName, isoName, VirtualDriveFileName
| rename ContextTimeStamp_decimal as endpointSystemClock, aid as agentID, ComputerName as computerName, VolumeDriveLetter as driveLetter, VolumeName as volumeName, VirtualDriveFileName as fullPath
| convert ctime(endpointSystemClock)
```

## Query 4
```cql
event_platform=win event_simpleName IN (FsVolumeMounted, RemovableMediaVolumeMounted, SnapshotVolumeMounted) VirtualDriveFileType_decimal=1 
| rex field=VirtualDriveFileName ".*\\\(?<isoName>.*\.(img|iso))" 
| table ContextTimeStamp_decimal, aid, ComputerName, VolumeDriveLetter, VolumeName, isoName, VirtualDriveFileName
| rename ContextTimeStamp_decimal as endpointSystemClock, aid as agentID, ComputerName as computerName, VolumeDriveLetter as driveLetter, VolumeName as volumeName, VirtualDriveFileName as fullPath
| convert ctime(endpointSystemClock)
```

## Query 5
```cql
event_platform=win event_simpleName IN (FsVolumeMounted, RemovableMediaVolumeMounted, SnapshotVolumeMounted) VirtualDriveFileType_decimal=1 
| rex field=VirtualDriveFileName ".*\\\(?<isoName>.*\.(img|iso))" 
| search isoName!="SW_DVD5_OFFICE_PROFESSIONAL_PLUS_64BIT_ENGLISH_-6_OFFICEONLINESVR_MLF_X21-90444.iso"
```

## Query 6
```cql
event_platform=win event_simpleName IN (FsVolumeMounted, RemovableMediaVolumeMounted, SnapshotVolumeMounted) VirtualDriveFileType_decimal=1 
| rex field=VirtualDriveFileName ".*\\\(?<isoName>.*\.(img|iso))" 
| regex isoName!="sw_dvd\d\_office\_professional\_plus\_(64|32)bit\_english\_\-\d\_officeonlinesvr_mlf_x\d+\-\d+\.iso"
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> The ISO has to be mounted - via double clicking - and the Falcon sensor has to be at version 6.40+.
— [CS] Andrew-CS · score 1

### Q&A

**Q — [Community] jarks_20:** In the case of legit .iso images, what would be the best approach to the detection? Adding exclusions on the search manually would make the week longer :) How to determine if this .iso is not one of ours or externally sent? Does this make sense?

**A — [CS] Andrew-CS:** Any commonality to the ISOs that are yours? Naming conventions, computers interacting with them, location, etc.?
