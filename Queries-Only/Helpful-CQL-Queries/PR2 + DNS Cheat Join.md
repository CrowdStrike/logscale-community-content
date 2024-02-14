```

(#event_simpleName = ProcessRollup2 AND ImageFileName = /.*\\powershell\.exe/) OR (#event_simpleName=DnsRequest AND (DomainName!="ocsp.digicert.com" AND DomainName!="localhost"))

| rename("ContextProcessId",as="TargetProcessId")
| groupby([aid, TargetProcessId], function=stats([count(#event_simpleName, distinct=true), collect(DomainName), collect(ImageFileName), collect(CommandLine)]), limit=max)
| _count > 1
| ImageFileName=/.*\\(?<fileName>.*\.exe)/
| "Process Explorer" := format("[Process Explorer](https://falcon.crowdstrike.com/investigate/process-explorer/%s/%s)", field=[aid, TargetProcessId])
| table([aid, DomainName, fileName, CommandLine, "Process Explorer"])

```

OR

```
#event_simpleName=/(ProcessRollup2|DnsRequest)/ event_platform=Win

| case{TargetProcessId="*" | falconPID:=TargetProcessId; ContextProcessId="*" | falconPID:=ContextProcessId}
| regex("\\\(?<fileName>\w+\.\w{3})", field=ImageFileName, strict=false)
| groupBy([aid, falconPID], function=([collect([fileName, CommandLine, DomainName]), count(#event_simpleName, distinct=true, as="eventCount")]))
| eventCount=2

```

OR

```

(#event_simpleName=ProcessRollup2 AND event_platform=Win) OR (#event_simpleName=DnsRequest AND event_platform=Win)

| #event_simpleName match {

    ProcessRollup2 => rename(field=TargetProcessId, as=falconPID);
    *              => rename(field=ContextProcessId, as=falconPID);
}

| selfJoinFilter([aid,falconPID], where=[

    {#event_simpleName = ProcessRollup2},
    {#event_simpleName = DnsRequest}
  ], prefilter = True
)

| groupBy([aid, falconPID], function=[count(#event_simpleName, distinct=true),collect([#event_simpleName, ImageFileName, DomainName, UserSid], limit=524288)], limit=max)
| _count = 2

```