```
// Get alert events
#repo=detections (ExternalApiType=/Event_(Epp|Idp|Mobile)DetectionSummaryEvent/) OR (ExternalApiType=Event_UserActivityAuditEvent OperationName=detection_update)
| case{
    ExternalApiType=Event_UserActivityAuditEvent Attributes.update_status="closed" | ResolveTime:=@timestamp;
    ExternalApiType=Event_UserActivityAuditEvent | UpdateTime:=@timestamp;
    * | DetectTime:=@timestamp;
}

// Normalize alert UUID
| detectID:=Attributes.composite_id 
| detectID:=CompositeId

// Perform aggregation
| groupBy([detectID], function=([count(ExternalApiType, distinct=true), min(DetectTime, as=DetectTime), min(UpdateTime, as=UpdateTime), max(ResolveTime, as=ResolveTime), selectLast([Attributes.update_status, Attributes.add_tag, Severity, SeverityName])]), limit=max)

// Only evaluablue closed alerts
| Attributes.update_status="closed"

// Calculate Mean Time To React in millis
| MTTReact:=UpdateTime-DetectTime

// Calucuate Mean Time To Respond in millis
| MTTRespond:=ResolveTime-UpdateTime

// Calculate Mean Time To Resolve in millis
| MTTResolve:=ResolveTime-DetectTime

// Aggregate by Severity
| case{
    Severity<20 | Sev:="1";
    Severity<40 | Sev:="2";
    Severity<60 | Sev:="3";
    Severity<80 | Sev:="4";
    Severity<100 | Sev:="5";
}
| groupBy([Sev, SeverityName], function=([count(detectID, as=SampleSize), avg(MTTReact, as=MTTReact), avg(MTTRespond, as=MTTRespond), avg(MTTResolve, as=MTTResolve)]))
| SeverityName=*
| sort(Sev, order=desc) 
| drop([Sev])

// Make ouput pretty
| MTTReact:=round(MTTReact) | formatDuration(field=MTTReact, precision=3, as=MTTReact)
| MTTRespond:=round(MTTRespond) | formatDuration(field=MTTRespond, precision=3, as=MTTRespond)
| MTTResolve:=round(MTTResolve) | formatDuration(field=MTTResolve, precision=3, as=MTTResolve)
| rename([[MTTReact, React], [MTTRespond, Respond], [MTTResolve, Resolve]])
| default(value="-", field=[React, Respond, Resolve], replaceEmpty=true)
```