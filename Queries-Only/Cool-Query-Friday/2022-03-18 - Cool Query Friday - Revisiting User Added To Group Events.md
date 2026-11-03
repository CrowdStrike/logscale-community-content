---
title: "Revisiting User Added To Group Events"
date: 2022-03-18
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/th06gy/20220318_cool_query_friday_revisiting_user_added/"
mitre: []
series: Cool Query Friday
---

# Revisiting User Added To Group Events

> Source: [https://www.reddit.com/r/crowdstrike/comments/th06gy/20220318_cool_query_friday_revisiting_user_added/](https://www.reddit.com/r/crowdstrike/comments/th06gy/20220318_cool_query_friday_revisiting_user_added/) — by Andrew-CS (CrowdStrike) — 2022-03-18

Welcome to our fortieth(!!) installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
[...]
| eval falconPID=coalesce(TargetProcessId_decimal, RpcClientProcessId_decimal)
This takes the value of TargetProcessId_decimal, which exists in ProcessRollup2 events, and the value RpcClientProcessId_decimal, which exists in UserAccountAddedToGroup events, and makes a new variable named falconPID.
```

## Query 2
```cql
[...]
| rename UserName as responsibleUserName
| rename UserSid_readable as responsibleUserSID
```

## Query 3
```cql
[...]
| eval GroupRid_dec=tonumber(ltrim(tostring(GroupRid), "0"), 16)
| eval UserRid_dec=tonumber(ltrim(tostring(UserRid), "0"), 16)
| eval UserSid_readable=DomainSid. "-" .UserRid_dec
```

## Query 4
```cql
[...]
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName
| lookup local=true grouprid_wingroup.csv GroupRid_dec OUTPUT WinGroup
| fillnull value="-" UserName responsibleUserName
```

## Query 5
```cql
[...]
| stats dc(event_simpleName) as eventCount, values(ProcessStartTime_decimal) as processStartTime, values(FileName) as responsibleFile, values(CommandLine) as responsibleCmdLine, values(responsibleUserSID) as responsibleUserSID, values(responsibleUserName) as responsibleUserName, values(WinGroup) as windowsGroupName, values(GroupRid_dec) as windowsGroupRID, values(UserName) as addedUserName, values(UserSid_readable) as addedUserSID by aid, falconPID
| where eventCount>1
```

## Query 6
```cql
(index=main sourcetype=UserAccountAddedToGroup* event_platform=win event_simpleName=UserAccountAddedToGroup) OR (index=main sourcetype=ProcessRollup2* event_platform=win event_simpleName=ProcessRollup2)
| eval falconPID=coalesce(TargetProcessId_decimal, RpcClientProcessId_decimal)
| rename UserName as responsibleUserName
| rename UserSid_readable as responsibleUserSID
| eval GroupRid_dec=tonumber(ltrim(tostring(GroupRid), "0"), 16)
| eval UserRid_dec=tonumber(ltrim(tostring(UserRid), "0"), 16)
| eval UserSid_readable=DomainSid. "-" .UserRid_dec
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName
| lookup local=true grouprid_wingroup.csv GroupRid_dec OUTPUT WinGroup
| fillnull value="-" UserName responsibleUserName
| stats dc(event_simpleName) as eventCount, values(ProcessStartTime_decimal) as processStartTime, values(FileName) as responsibleFile, values(CommandLine) as responsibleCmdLine, values(responsibleUserSID) as responsibleUserSID, values(responsibleUserName) as responsibleUserName, values(WinGroup) as windowsGroupName, values(GroupRid_dec) as windowsGroupRID, values(UserName) as addedUserName, values(UserSid_readable) as addedUserSID by aid, falconPID
| where eventCount>1
```

## Query 7
```cql
[...]
| eval ProcExplorer=case(falconPID!="","https://falcon.us-2.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
| convert ctime(processStartTime)
| table processStartTime, aid, responsibleUserSID, responsibleUserName, responsibleFile, responsibleCmdLine, addedUserSID, addedUserName, windowsGroupRID, windowsGroupName, ProcExplorer
```

## Query 8
```cql
(index=main sourcetype=UserAccountAddedToGroup* event_platform=win event_simpleName=UserAccountAddedToGroup) OR (index=main sourcetype=ProcessRollup2* event_platform=win event_simpleName=ProcessRollup2)
| eval falconPID=coalesce(TargetProcessId_decimal, RpcClientProcessId_decimal)
| rename UserName as responsibleUserName
| rename UserSid_readable as responsibleUserSID
| eval GroupRid_dec=tonumber(ltrim(tostring(GroupRid), "0"), 16)
| eval UserRid_dec=tonumber(ltrim(tostring(UserRid), "0"), 16)
| eval UserSid_readable=DomainSid. "-" .UserRid_dec
| lookup local=true userinfo.csv UserSid_readable OUTPUT UserName
| lookup local=true grouprid_wingroup.csv GroupRid_dec OUTPUT WinGroup
| fillnull value="-" UserName responsibleUserName
| stats dc(event_simpleName) as eventCount, values(ProcessStartTime_decimal) as processStartTime, values(FileName) as responsibleFile, values(CommandLine) as responsibleCmdLine, values(responsibleUserSID) as responsibleUserSID, values(responsibleUserName) as responsibleUserName, values(WinGroup) as windowsGroupName, values(GroupRid_dec) as windowsGroupRID, values(UserName) as addedUserName, values(UserSid_readable) as addedUserSID by aid, falconPID
| where eventCount>1 
| eval ProcExplorer=case(falconPID!="","https://falcon.us-2.crowdstrike.com/investigate/process-explorer/" .aid. "/" . falconPID)
| convert ctime(processStartTime)
| table processStartTime, aid, responsibleUserSID, responsibleUserName, responsibleFile, responsibleCmdLine, addedUserSID, addedUserName, windowsGroupRID, windowsGroupName, ProcExplorer
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> Nice! For performance reasons, you may want to add the additional search parameters to the first line like this: (index=main sourcetype=UserAccountAddedToGroup* event_platform=win event_simpleName=UserAccountAddedToGroup) OR (index=main sourcetype=ProcessRollup2* event_platform=win event_simpleName=ProcessRollup2 ProductType=1 FileName!=VSFinalizer.exe) That will qualify out more results quicker :)
— [CS] Andrew-CS · score 2

> Not exactly sure. If you have a massive environment it maybe it's running for too long? What happens if you shorted the search period a bit?
— [CS] Andrew-CS · score 1

### Q&A

**Q — [Community] amjcyb:** With this and the older one ([https://www.reddit.com/r/crowdstrike/comments/o2onsf/20210618\_cool\_query\_friday\_user\_added\_to\_group/](https://www.reddit.com/r/crowdstrike/comments/o2onsf/20210618_cool_query_friday_user_added_to_group/)) we get lots of "UserName: Unknown". We check the SID and t …

**A — [CS] Andrew-CS:** The user was added then deleted. The user was added, but never logged in to that system (so you'll have SID, but the UserLogon event will never have occurred which helps populate UserName).

**Q — [Community] yankeesfan01x:** The grand finale query threw back over 23,000 events for me in a 15 minutes time frame so I'm not sure what I'm doing wrong with this one?

**A — [CS] Andrew-CS:** The number of events (if you're looking at the number value in the "Events" tab) will be very high as we're looking at all process executions. Are you saying the table has 23K user additions in it? That would be crazy.

**Q — [Community] yankeesfan01x:** That's my bad. The high number is showing in the events tab but nothing is showing in the statistics tab. You might need to correct me if I'm wrong here but the statistics tab will actually show if a user account has been added to a user group on a Windows host? If I created a scheduled search to al …

**A — [CS] Andrew-CS:** The "grand finale" is actually marrying the process that did the adding with the add itself. If you don't care about the process that did the adding, but care more about what was added, you can use the [older CQF](https://www.reddit.com/r/crowdstrike/comments/o2onsf/20210618_cool_query_friday_user_added_to_group/). That will be easier and the query will be faster.
