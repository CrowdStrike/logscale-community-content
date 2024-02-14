```
#event_simpleName=ProcessRollup2

| join({#event_simpleName=FirewallSetRule}, key=ContextProcessId, field=TargetProcessId, include=[FirewallRule, FirewallRuleId])
| ImageFileName=/.*\\(?<fileName>.*\..*)/
| table([aid, UserSid, fileName, FirewallRuleId, FirewallRule, ImageFileName, CommandLine])

```