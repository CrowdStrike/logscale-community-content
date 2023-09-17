```
| selfJoinFilter([aid, falconPID], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=DnsRequest}], prefilter=true)
```

Example usage to merge events:

```
event_platform=Win #event_simpleName=/^(ProcessRollup2|DnsRequest)$/
| falconPID := TargetProcessId
| falconPID := ContextProcessId
| selfJoinFilter([aid, falconPID], where=[{#event_simpleName=ProcessRollup2}, {#event_simpleName=DnsRequest}], prefilter=true)
| groupBy([aid, falconPID], function=([count(#event_simpleName, distinct=true, as=eventCount), collect([ParentBaseFileName, ImageFileName, CommandLine])]))
| test(eventCount==2)
```

[selfJoinFilter Documentation](https://library.humio.com/data-analysis/functions-selfjoinfilter.html)
