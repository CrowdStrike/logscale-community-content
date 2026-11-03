---
title: "PSFalcon, Bulk RTR Queuing, and STDOUT Redirection to LogScale"
date: 2022-11-03
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/yl8hv8/20221103_cool_query_friday_psfalcon_bulk_rtr/"
mitre: []
series: Cool Query Friday
---

# PSFalcon, Bulk RTR Queuing, and STDOUT Redirection to LogScale

> Source: [https://www.reddit.com/r/crowdstrike/comments/yl8hv8/20221103_cool_query_friday_psfalcon_bulk_rtr/](https://www.reddit.com/r/crowdstrike/comments/yl8hv8/20221103_cool_query_friday_psfalcon_bulk_rtr/) — by Andrew-CS (CrowdStrike) — 2022-11-03

Welcome to our fifty-second installment of [Cool Query Friday](https://www.reddit.com/r/crowdstrike/collection/8016c539-c284-442c-9726-6bc05053d7a9/). The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
Get-FalconHost -Filter "platform_name:'Windows'" -All | Invoke-FalconRtr -Command runscript -Argument "-CloudFile='list-browser-extensions'" -QueueOffline $true
```

## Query 2
```cql
| format(format="%s | %s | %s", field=[Name,  Version, Id], as="pluginDetails")
| groupBy([aid, host, Browser], function=stats(collect([pluginDetails])))
```

## Query 3
```cql
Get-FalconHost -Limit 100 -Detailed | Send-FalconEvent
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Q&A

**Q — [Community] netsec_:** How do you get the results from this if you don't?

**A — [CS] Andrew-CS:** You can always issue bulk RTR commands using PSFalcon and then invoke `Get-FalconQueue` to view the results.

**Q — [Community] big_mic_energy:** How does this setup differ if Falcon and LogScale are products we already own? Keeping in mind I am an admin for both products and Falcon has been collecting data for years now.

**A — [CS] Andrew-CS:** You can just have Falcon redirect the RTR output to the LogScale instance you have running. You just have to make sure your URL is correct as is outlined in this section: >Copy the URL under “Ingest host name” as well. You can just follow my lead if you’re using Community Edition, however, if you’re a full LogScale customer this URL will be different so please make note of it.
