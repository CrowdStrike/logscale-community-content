---
title: "Auto-Enriching Alerts with Bespoke Raptor Queries and Fusion SOAR Workflows"
date: 2024-05-30
author: "Andrew-CS"
source_url: "https://www.reddit.com/r/crowdstrike/comments/1d46szz/20240530_cool_query_friday_autoenriching_alerts/"
mitre: []
series: Cool Query Friday
---

# Auto-Enriching Alerts with Bespoke Raptor Queries and Fusion SOAR Workflows

> Source: [https://www.reddit.com/r/crowdstrike/comments/1d46szz/20240530_cool_query_friday_autoenriching_alerts/](https://www.reddit.com/r/crowdstrike/comments/1d46szz/20240530_cool_query_friday_autoenriching_alerts/) — by Andrew-CS (CrowdStrike) — 2024-05-30

Welcome to our seventy-fourth installment of Cool Query Friday. The format will be: (1) description of what we're doing (2) walk through of each step (3) application in the wild.

## Query 1
```cql
// Create parameter for Agent ID; Get AssociateIndicator Events and ProcessRollup2 Events
aid=?aid (#event_simpleName=AssociateIndicator OR #event_simpleName=ProcessRollup2)
// Use selfJoinFilter to join events
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName=AssociateIndicator}, {#event_simpleName=ProcessRollup2}])
```

## Query 2
```cql
// Create parameter for Agent ID; Get AssociateIndicator Events and ProcessRollup2 Events
aid=?aid (#event_simpleName=AssociateIndicator OR #event_simpleName=ProcessRollup2)
// Use selfJoinFilter to join events
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName=AssociateIndicator}, {#event_simpleName=ProcessRollup2}])
// Create pretty process tree for ProcessRollup2 events
| case {
#event_simpleName="ProcessRollup2" | ExecutionChain:=format(format="%s → %s (%s)", field=[ParentBaseFileName, FileName, RawProcessId]);
*;
}
// Use groupBy to aggregate
| groupBy([aid, TargetProcessId], function=([count(aid, as=Occurrences), selectFromMin(field="@timestamp", include=[@timestamp]), collect([ComputerName, UserName, ExecutionChain, Tactic, Technique, DetectDescription, CommandLine])]))
```

## Query 3
```cql
// Create parameter for Agent ID; Get AssociateIndicator Events and ProcessRollup2 Events
aid=?aid (#event_simpleName=AssociateIndicator OR #event_simpleName=ProcessRollup2)
// Use selfJoinFilter to join events
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName=AssociateIndicator}, {#event_simpleName=ProcessRollup2}])
// Create pretty process tree for ProcessRollup2 events
| case {
#event_simpleName="ProcessRollup2" | ExecutionChain:=format(format="%s → %s (%s)", field=[ParentBaseFileName, FileName, RawProcessId]);
*;
}
// Use groupBy to aggregate
| groupBy([aid, TargetProcessId], function=([count(aid, as=Occurrences), selectFromMin(field="@timestamp", include=[@timestamp]), collect([ComputerName, UserName, ExecutionChain, Tactic, Technique, DetectDescription, CommandLine])]))
// Add Process Tree link to ease investigation; Uncomment your cloud
| rootURL := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Process Explorer](%sgraphs/process-explorer/tree?id=pid:%s:%s)", field=["rootURL", "aid", "TargetProcessId"], as="Falcon")
| drop([rootURL])
| sort(@timestamp, order=desc, limit=20000)
```

## Community & Staff Additions
*Harvested from this post's [r/CrowdStrike](https://www.reddit.com/r/crowdstrike/) comment thread — not part of the original CQF post. **[CS]** = CrowdStrike staff · **[Community]** = other r/CrowdStrike users. Upvote scores shown for context.*

### Query variants

```cql
| groupBy([aid, TargetProcessId], function=([count(aid, as=Occurrences), selectFromMin(field="@timestamp", include=[@timestamp]), collect([ComputerName, UserName, ExecutionChain, Tactic, Technique, DetectDescription, CommandLine])]))
```
— [CS] Andrew-CS · comment score 2

```cql
| groupBy([aid, TargetProcessId], function=([count(aid, as=Occurrences), selectFromMin(field="@timestamp", include=[@timestamp]), collect([ComputerName, UserName, ExecutionChain, Tactic, Technique, DetectDescription, CommandLine])]), limit=max)
```
— [CS] Andrew-CS · comment score 2

### Operational caveats

> Comments have a certain size limit and adding raw syntax will likely always break that limit. The comments section isn't really designed to show JSON. You might be able to link to the workflow execution URL so you can quickly pivot to the formatted results.
— [CS] Andrew-CS · score 1

### Q&A

**Q — [Community] xplorationz:** Can you trigger Fusion workflow using API? and get output via API. (New to Falcon)

**A — [CS] bk-CS:** Yes, on-demand fusion workflows can be triggered using `POST /workflows/entities/execute/v1`. You can separate the event search portion of Andrew's example into an on-demand workflow which would allow you to trigger it via API and also call it in a detection-triggered workflow.
