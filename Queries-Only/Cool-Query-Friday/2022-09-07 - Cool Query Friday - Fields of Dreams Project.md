---
title: "Fields of Dreams Project"
date: 2022-09-07
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/x85ufw/20220907_cool_query_friday_fields_of_dreams/"
mitre: []
series: Cool Query Friday
---

# Fields of Dreams Project

> Source: [https://www.reddit.com/r/crowdstrike/comments/x85ufw/20220907_cool_query_friday_fields_of_dreams/](https://www.reddit.com/r/crowdstrike/comments/x85ufw/20220907_cool_query_friday_fields_of_dreams/) — by Andrew-CS (CrowdStrike) — 2022-09-07

Welcome to our forty-eighth installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
| eval LogonType=case(
	LogonType_decimal="2",  "Interactive", 
	LogonType_decimal="3",  "Network", 
	LogonType_decimal="4",  "Batch", 
	LogonType_decimal="5",  "Service", 
	LogonType_decimal="6",  "Proxy", 
	LogonType_decimal="7",  "Unlock", 
	LogonType_decimal="8",  "Network Cleartext", 
	LogonType_decimal="9",  "New Credentials", 
	LogonType_decimal="10", "Remote Interactive", 
	LogonType_decimal="11", "Cached Interactive", 
	LogonType_decimal="12", "Cached Remote Interactive", 
	LogonType_decimal="13", "Cached Unlock"
	)
```

## Query 2
```cql
| eval LogonType=case(LogonType_decimal="2", "Interactive", LogonType_decimal="3",  "Network", LogonType_decimal="4", "Batch", LogonType_decimal="5", "Service", LogonType_decimal="6", "Proxy", LogonType_decimal="7", "Unlock", LogonType_decimal="8", "Network Cleartext", LogonType_decimal="9", "New Credentials", LogonType_decimal="10", "Remote Interactive", LogonType_decimal="11", "Cached Interactive", LogonType_decimal="12", "Cached Remote Interactive", LogonType_decimal="13", "Cached Unlock")
```
