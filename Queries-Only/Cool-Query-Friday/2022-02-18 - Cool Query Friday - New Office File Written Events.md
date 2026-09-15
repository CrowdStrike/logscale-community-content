---
title: "New Office File Written Events"
date: 2022-02-18
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/svf8y7/20220218_cool_query_friday_new_office_file/"
mitre: []
series: Cool Query Friday
---

# New Office File Written Events

> Source: [https://www.reddit.com/r/crowdstrike/comments/svf8y7/20220218_cool_query_friday_new_office_file/](https://www.reddit.com/r/crowdstrike/comments/svf8y7/20220218_cool_query_friday_new_office_file/) — by Andrew-CS (CrowdStrike) — 2022-02-18

Welcome to our thirty-seventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
event_simpleName IN (MSDocxFileWritten, MSPptxFileWritten, MSVsdxFileWritten, MSXlsxFileWritten)
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal)
```

## Query 2
```cql
[...]
| eval MSOfficeSubType=case(MSOfficeSubType_decimal=0, "Unknown", MSOfficeSubType_decimal=1, "Legacy Binary", MSOfficeSubType_decimal=2, "OOXML")
```

## Query 3
```cql
[...]
| eval isInOutlookTemp=if(match(TargetFileName, ".*\\\Content\.Outlook\\\.*"),"Yes", "No")
| eval isInDownloads=if(match(TargetFileName, ".*\\\Downloads\\\.*"),"Yes", "No")
```

## Query 4
```cql
[...]
| eval isOnRemoveableDrive=case(IsOnRemovableDisk_decimal=1, "Yes", IsOnRemovableDisk_decimal=0, "No")
| eval isOnNetworkDrive=case(IsOnNetwork_decimal=1, "Yes", IsOnNetwork_decimal=0, "No")
```

## Query 5
```cql
[...]
| rex field=FileName ".*\.(?<fileExtension>.*)"
| eval fileExtension=lower(fileExtension)
```

## Query 6
```cql
[...]
| rex mode=sed field=FilePath "s/\\\Device\\\HarddiskVolume\d+//g"
```

## Query 7
```cql
[...]
| rex mode=sed field=FilePath "s/\\\Device\\\HarddiskVolume\d+/C:/g"
```

## Query 8
```cql
[...]
| eval ProcExplorer=case(falconPID!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
```

## Query 9
```cql
[...]
| rename FileOperatorSid_readable AS UserSid_readable
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName, AccountType, LocalAdminAccess
```

## Query 10
```cql
[...]
| table aid, ComputerName, UserSid_readable, UserName, AccountType, LocalAdminAccess, ContextTimeStamp_decimal, fileExtension, MSOfficeSubType, FileName, FilePath, isIn*, isOn*, ProcExplorer 
| convert ctime(ContextTimeStamp_decimal)
| rename aid as "Falcon AID", ComputerName as "Endpoint", UserSid_readable as "User SID", UserName as "User", AccountType as "Account Type", LocalAdminAccess as "Local Admin?", ContextTimeStamp_decimal as "File Written Time", fileExtension as "Extension", MSOfficeSubType as "Office Type", isInDownloads as "Downloads Folder?", isInOutlookTemp as "Outlook Temp?", isOnNetworkDrive as "Network Drive?", isOnRemoveableDrive as "Removable Drive?", ProcExplorer as "Process Explorer Link"
```

## Query 11
```cql
event_simpleName IN (MSDocxFileWritten, MSPptxFileWritten, MSVsdxFileWritten, MSXlsxFileWritten)
| eval falconPID=coalesce(ContextProcessId_decimal, TargetProcessId_decimal)
| eval MSOfficeSubType=case(MSOfficeSubType_decimal=0, "Unknown", MSOfficeSubType_decimal=1, "Legacy Binary", MSOfficeSubType_decimal=2, "OOXML") 
| eval isInOutlookTemp=if(match(TargetFileName, ".*\\\Content\.Outlook\\\.*"),"Yes", "No")
| eval isInDownloads=if(match(TargetFileName, ".*\\\Downloads\\\.*"),"Yes", "No")
| eval isOnRemoveableDrive=case(IsOnRemovableDisk_decimal=1, "Yes", IsOnRemovableDisk_decimal=0, "No")
| eval isOnNetworkDrive=case(IsOnNetwork_decimal=1, "Yes", IsOnNetwork_decimal=0, "No")
| rex field=FileName ".*\.(?<fileExtension>.*)"
| eval fileExtension=lower(fileExtension)
| rex mode=sed field=FilePath "s/\\\Device\\\HarddiskVolume\d+/C:/g"
| eval ProcExplorer=case(falconPID!="","https://falcon.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
| rename FileOperatorSid_readable AS UserSid_readable
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName, AccountType, LocalAdminAccess
| table aid, ComputerName, UserSid_readable, UserName, AccountType, LocalAdminAccess, ContextTimeStamp_decimal, fileExtension, MSOfficeSubType, FileName, FilePath, isIn*, isOn*, ProcExplorer 
| convert ctime(ContextTimeStamp_decimal)
| rename aid as "Falcon AID", ComputerName as "Endpoint", UserSid_readable as "User SID", UserName as "User", AccountType as "Account Type", LocalAdminAccess as "Local Admin?", ContextTimeStamp_decimal as "File Written Time", fileExtension as "Extension", MSOfficeSubType as "Office Type", isInDownloads as "Downloads Folder?", isInOutlookTemp as "Outlook Temp?", isOnNetworkDrive as "Network Drive?", isOnRemoveableDrive as "Removable Drive?", ProcExplorer as "Process Explorer Link"
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName, AccountType, LocalAdminAccess
```
— [CS] Andrew-CS · comment score 1
