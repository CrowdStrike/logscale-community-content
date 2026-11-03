---
title: "explain:asTable()"
date: 2026-03-20
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1ryw8kr/20260320_cool_query_friday_explainastable/"
mitre: []
series: Cool Query Friday
---

# explain:asTable()

> Source: [https://www.reddit.com/r/crowdstrike/comments/1ryw8kr/20260320_cool_query_friday_explainastable/](https://www.reddit.com/r/crowdstrike/comments/1ryw8kr/20260320_cool_query_friday_explainastable/) — by Andrew-CS (CrowdStrike) — 2026-03-20

Welcome to our [eighty-eighth](https://www.youtube.com/watch?v=HWoW-vX4HT8) installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

```cql
#event_simpleName=ProcessRollup2 
| CommandLine=/\-(e(nc|ncodedcommand|ncoded)?)\s+/iF
| groupBy([ComputerName, event_platform], function=([count(CommandLine, distinct=true, as=uniqueCmdLines), count(aid, as=totalExecutions)]), limit=max)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Operational caveats

> I would say if you're running a job nightly, I might break this into two jobs... (1) Historic: after you've looked for an IOC for 30-days, you only need to search new data for those same IOCs (in your case, the past 24-hours). (2) New: when you get a new IOC, you need to look back once thirty days and then only moving forward. Does that make sense? If the IOCs are atomic (SHA256, IP, Domain) I might leverage the IOC functionality in Falcon so you're alerted in real-time as opposed to searching. Things like Custom IOAs can also be helpful for file names, command line fragments, etc.
— [CS] Andrew-CS · score 1
