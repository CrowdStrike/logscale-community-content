---
title: "Scoring User Logon Events in Windows"
date: 2022-04-08
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/tz5obg/20220408_cool_query_friday_scoring_user_logon/"
mitre: []
series: Cool Query Friday
---

# Scoring User Logon Events in Windows

> Source: [https://www.reddit.com/r/crowdstrike/comments/tz5obg/20220408_cool_query_friday_scoring_user_logon/](https://www.reddit.com/r/crowdstrike/comments/tz5obg/20220408_cool_query_friday_scoring_user_logon/) — by Andrew-CS (CrowdStrike) — 2022-04-08

Welcome to our forty-first installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
index=main sourcetype=UserLogon* event_simpleName=UserLogon event_platform=win
| search UserSid_readable=S-1-5-21-* AND LogonType_decimal!=7
```

## Query 2
```cql
[...]
| lookup local=true userinfo.csv UserSid_readable OUTPUT AccountType, LocalAdminAccess
```

## Query 3
```cql
| inputlookup userinfo.csv
```

## Query 4
```cql
[...]
| lookup local=true aid_master aid OUTPUT Version, AgentVersion
```

## Query 5
```cql
| inputlookup aid_master
```

## Query 6
```cql
[...]
| eval passwordAgeDays=round((now()-PasswordLastSet_decimal)/60/60/24,0) 
| fillnull passwordAgeDays value="NA"
```

## Query 7
```cql
[...]
| iplocation RemoteAddressIP4
```

## Query 8
```cql
[...]
| eval ratingRdpToDc=if(ProductType=2 AND LogonType_decimal=10,"10","0")
```

## Query 9
```cql
[...]
| eval ratingServiceAccountInteractive=case(UserName LIKE "svc%" AND (LogonType_decimal=2 OR LogonType_decimal=10), "10")
| fillnull ratingServiceAccountInteractive value=0
```

## Query 10
```cql
[...]
| eval ratingInteractiveServer=if(ProductType=3 AND LogonType_decimal=2,"3","0")
```

## Query 11
```cql
[...]
| eval ratingExternalRDP=if(isnotnull(Country) AND LogonType_decimal=10,"5","0")
```

## Query 12
```cql
[...]
| eval ratingPasswdAge=if(passwordAgeDays > 180,"3","0")
```

## Query 13
```cql
[...]
| eval ratingDomainAdmin=if(AccountType="Domain Administrators", "2", "0")
```

## Query 14
```cql
[...]
| eval weirdnessCoefficient=ratingRdpToDc + ratingServiceAccountInteractive + ratingRdpToDc + ratingInteractiveServer + ratingexternalRDP + ratingPasswdAge + ratingDomainAdmin
| table LogonTime_decimal, aid, ComputerName, Version, AgentVersion, UserName, UserSid_readable, LogonType_decimal, AccountType, LocalAdminAccess, ratingPasswdAge, weirdnessCoefficient 
| sort -weirdnessCoefficient, +LogonTime_decimal 
| convert ctime(LogonTime_decimal)
| rename LogonTime_decimal as "Logon Time", aid as "Falcon AID", ComputerName as "Endpoint", Version as "OS", AgentVersion as "Falcon Version", UserName as "User", UserSid_readable as "User SID", LogonType_decimal as "Logon Type", AccountType as "Account Type", LocalAdminAccess as "Local Admin?", ratingPasswdAge as "Password Age (Days)", weirdnessCoefficient as "Rating"
```

## Query 15
```cql
index=main sourcetype=UserLogon* event_simpleName=UserLogon event_platform=win 
| search UserSid_readable=S-1-5-21-* AND LogonType_decimal!=7
| lookup local=true userinfo.csv UserSid_readable OUTPUT AccountType, LocalAdminAccess 
| lookup local=true aid_master aid OUTPUT Version, AgentVersion 
| eval passwordAgeDays=round((now()-PasswordLastSet_decimal)/60/60/24,0) 
| fillnull passwordAgeDays value="NA" 
| iplocation RemoteAddressIP4 
| eval ratingRdpToDc=if(ProductType=2 AND LogonType_decimal=10,"10","0") 
| eval ratingServiceAccountInteractive=case(UserName LIKE "svc%" AND (LogonType_decimal=2 OR LogonType_decimal=10), "10") 
| fillnull ratingServiceAccountInteractive value=0 
| eval ratingRdpToDc=if(ProductType=2 AND LogonType_decimal=10,"10","0") 
| eval ratingInteractiveServer=if(ProductType=3 AND LogonType_decimal=2,"3","0") 
| eval ratingexternalRDP=if(isnotnull(Country) AND LogonType_decimal=10,"5","0") 
| eval ratingPasswdAge=if(passwordAgeDays > 180,"3","0") 
| eval ratingDomainAdmin=if(AccountType="Domain Administrators", "2", "0")
| eval weirdnessCoefficient=ratingServiceAccountInteractive + ratingRdpToDc + ratingInteractiveServer + ratingexternalRDP + ratingPasswdAge + ratingDomainAdmin
| table LogonTime_decimal, aid, ComputerName, Version, AgentVersion, UserName, UserSid_readable, LogonType_decimal, AccountType, LocalAdminAccess, ratingPasswdAge, weirdnessCoefficient 
| sort -weirdnessCoefficient, +LogonTime_decimal 
| convert ctime(LogonTime_decimal)
| rename LogonTime_decimal as "Logon Time", aid as "Falcon AID", ComputerName as "Endpoint", Version as "OS", AgentVersion as "Falcon Version", UserName as "User", UserSid_readable as "User SID", LogonType_decimal as "Logon Type", AccountType as "Account Type", LocalAdminAccess as "Local Admin?", ratingPasswdAge as "Password Age (Days)", weirdnessCoefficient as "Rating"
```

## Query 16
```cql
index=main sourcetype=UserLogon* event_simpleName=UserLogon event_platform=win 
| search UserSid_readable=S-1-5-21-* AND LogonType_decimal!=7
| lookup local=true userinfo.csv UserSid_readable OUTPUT AccountType, LocalAdminAccess 
| lookup local=true aid_master aid OUTPUT Version, AgentVersion 
| eval passwordAgeDays=round((now()-PasswordLastSet_decimal)/60/60/24,0) 
| fillnull passwordAgeDays value="NA" 
| iplocation RemoteAddressIP4 
| eval ratingRdpToDc=if(ProductType=2 AND LogonType_decimal=10,"10","0") 
| eval ratingServiceAccountInteractive=case(UserName LIKE "svc%" AND (LogonType_decimal=2 OR LogonType_decimal=10), "10") 
| fillnull ratingServiceAccountInteractive value=0 
| eval ratingRdpToDc=if(ProductType=2 AND LogonType_decimal=10,"10","0") 
| eval ratingInteractiveServer=if(ProductType=3 AND LogonType_decimal=2,"3","0") 
| eval ratingexternalRDP=if(isnotnull(Country) AND LogonType_decimal=10,"5","0") 
| eval ratingPasswdAge=if(passwordAgeDays > 180,"3","0") 
| eval ratingDomainAdmin=if(AccountType="Domain Administrators", "2", "0")
| eval weirdnessCoefficient=ratingServiceAccountInteractive + ratingRdpToDc + ratingInteractiveServer + ratingexternalRDP + ratingPasswdAge + ratingDomainAdmin
| table LogonTime_decimal, aid, ComputerName, Version, AgentVersion, UserName, UserSid_readable, LogonType_decimal, AccountType, LocalAdminAccess, ratingPasswdAge, weirdnessCoefficient 
| stats sum(weirdnessCoefficient) as weirdnessCoefficient, dc(aid) as uniqueEndpoints, count(aid) as totalLogons by UserSid_readable, UserName, AccountType 
| sort - weirdnessCoefficient
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| eval weirdnessCoefficient=ratingServiceAccountInteractive + ratingRdpToDc + ratingInteractiveServer + ratingexternalRDP + ratingPasswdAge + ratingDomainAdmin
```
— [CS] Andrew-CS · comment score 1

### Q&A

**Q — [Community] kevinelwell:** You can register for free here: [https://mitre.brandlive.com/mitre-attackcon-3/en](https://mitre.brandlive.com/mitre-attackcon-3/en) The presenter was Halee Mills **Tracking Noisy Behavior and Risk-Based Alerting with ATT&CK** Having ATT&CK to identify threats, prioritize data sources, and improve s …

**A — [CS] Andrew-CS:** Oh yeah! Thanks. Fixed. It was counted twice in this line: | eval weirdnessCoefficient=ratingServiceAccountInteractive + ratingRdpToDc + ratingInteractiveServer + ratingexternalRDP + ratingPasswdAge + ratingDomainAdmin
