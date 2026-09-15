---
title: "Password Age and Reused Local Passwords"
date: 2021-05-14
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/ncb5z7/20210514_cool_query_friday_password_age_and/"
mitre: []
series: Cool Query Friday
---

# Password Age and Reused Local Passwords

> Source: [https://www.reddit.com/r/crowdstrike/comments/ncb5z7/20210514_cool_query_friday_password_age_and/](https://www.reddit.com/r/crowdstrike/comments/ncb5z7/20210514_cool_query_friday_password_age_and/) — by Andrew-CS (CrowdStrike) — 2021-05-14

Welcome to our eleventh installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk though of each step (3) application in the wild.

## Query 1
```cql
| fields, aid, event_platform, ComputerName, LocalAddressIP4, LogonDomain, LogonServer, LogonTime_decimal, LogonType_decimal, PasswordLastSet_decimal, ProductType, UserIsAdmin_decimal, UserName, UserSid_readable
```

## Query 2
```cql
| where isnotnull(PasswordLastSet_decimal)
| eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_decimal="3", "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", LogonType_decimal="6", "Proxy", LogonType_decimal="7", "Unlock", LogonType_decimal="8", "Network Cleartext", LogonType_decimal="9", "New Credentials", LogonType_decimal="10", "RDP", LogonType_decimal="11", "Cached Credentials", LogonType_decimal="12", "Auditing", LogonType_decimal="13", "Unlock Workstation")
| eval Product=case(ProductType = "1","Workstation", ProductType = "2","Domain Controller", ProductType = "3","Server") 
| eval UserIsAdmin=case(UserIsAdmin_decimal = "1","Admin", UserIsAdmin_decimal = "0","Standard")
```

## Query 3
```cql
| eval passwordAge=now()-PasswordLastSet_decimal
```

## Query 4
```cql
| eval passwordAge=round(passwordAge/60/60/24,0)
```

## Query 5
```cql
| stats values(event_platform) as Platform latest(passwordAge) as passwordAge values(UserIsAdmin) as adminStatus by UserName, UserSid_readable
| sort - passwordAge
```

## Query 6
```cql
| where passwordAge > 179
```

## Query 7
```cql
event_simpleName=UserLogon
| where isnotnull(PasswordLastSet_decimal)
| fields, aid, event_platform, ComputerName, LocalAddressIP4, LogonDomain, LogonServer, LogonTime_decimal, LogonType_decimal, PasswordLastSet_decimal, ProductType, UserIsAdmin_decimal, UserName, UserSid_readable
| eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_decimal="3", "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", LogonType_decimal="6", "Proxy", LogonType_decimal="7", "Unlock", LogonType_decimal="8", "Network Cleartext", LogonType_decimal="9", "New Credentials", LogonType_decimal="10", "RDP", LogonType_decimal="11", "Cached Credentials", LogonType_decimal="12", "Auditing", LogonType_decimal="13", "Unlock Workstation")
| eval Product=case(ProductType = "1","Workstation", ProductType = "2","Domain Controller", ProductType = "3","Server") 
| eval UserIsAdmin=case(UserIsAdmin_decimal = "1","Admin", UserIsAdmin_decimal = "0","Standard")
| eval passwordAge=now()-PasswordLastSet_decimal
| eval passwordAge=round(passwordAge/60/60/24,0)
| stats values(event_platform) as Platform latest(passwordAge) as passwordAge values(UserIsAdmin) as adminStatus by UserName, UserSid_readable
| sort - passwordAge
| where passwordAge > 179
```

## Query 8
```cql
event_simpleName=UserLogon
| where isnotnull(PasswordLastSet_decimal)
| where LogonDomain=ComputerName
| stats dc(UserSid_readable) as distinctSID values(UserSid_readable) as userSIDs dc(UserName) as distinctUserNames values(UserName) as userNames count(aid) as totalLogins dc(aid) as distinctEndpoints by PasswordLastSet_decimal, event_platform
| sort - distinctEndpoints
| convert ctime(PasswordLastSet_decimal) 
| where distinctEndpoints > 1
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
event_simpleName=UserLogon
| eval UserName=lower(UserName) 
[...]
```
— [CS] Andrew-CS · comment score 1

```cql
event_simpleName=UserLogon UserIsAdmin_decimal=0
| where isnotnull(PasswordLastSet_decimal) | fields company, cid, aid, event_platform, ComputerName, LocalAddressIP4, LogonDomain, LogonServer, LogonTime_decimal, LogonType_decimal, PasswordLastSet_decimal, ProductType, UserIsAdmin_decimal, UserName, UserSid_readable | eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_decimal="3", "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", LogonType_decimal="6", "Proxy", LogonType_decimal="7", "Unlock", LogonType_decimal="8", "Network Cleartext", LogonType_decimal="9", "New Credentials", LogonType_decimal="10", "RDP", LogonType_decimal="11", "Cached Credentials", LogonType_decimal="12", "Auditing", LogonType_decimal="13", "Unlock Workstation") | eval Product=case(ProductType = "1","Workstation", ProductType = "2","Domain Controller", ProductType = "3","Server") | eval UserIsAdmin=case(UserIsAdmin_decimal = "1","Admin", UserIsAdmin_decimal = "0","Standard") | eval passwordAge=now()-PasswordLastSet_decimal | eval passwordAge=round(passwordAge/60/60/24,0) | stats values(event_platform) as Platform latest(passwordAge) as passwordAge values(UserIsAdmin) as adminStatus by UserName, UserSid_readable, company, cid | sort - passwordAge | where passwordAge > 179
```
— [CS] Andrew-CS · comment score 3

### Q&A

**Q — [Community] BinaryN1nja:** If you have multiple companies and you want to show that in the query...where would you put "company" to show in stats? Also, if you wanted to remove standard users where would you put | where adminStatus!=Standard ?

**A — [CS] Andrew-CS:** Hi there. Try this: event_simpleName=UserLogon UserIsAdmin_decimal=0 | where isnotnull(PasswordLastSet_decimal) | fields company, cid, aid, event_platform, ComputerName, LocalAddressIP4, LogonDomain, LogonServer, LogonTime_decimal, LogonType_decimal, PasswordLastSet_decimal, ProductType, UserIsAdmin_decimal, UserName, UserSid_readable | eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_decimal="3", "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", Log …

**Q — [Community] amjcyb:** If I didn't understund wrong this will get a username that has the same password in different endpoints, so it's nice to hunt for those localadmins with same password. But is it possible to hunt for different users with same password?

**A — [CS] Andrew-CS:** Hi there. What we're looking for here are local passwords that have an identical "last set" date right down to the microsecond. This works really well for local accounts that have been cloned onto a system via imaging or some other means, however... this does not cover all use cases where local admin accounts might share a password... If I set my local password to `fluffybunny11` and then you set your password to `fluffybunny11` a minute later, the "last set" date will be completely different bu …
