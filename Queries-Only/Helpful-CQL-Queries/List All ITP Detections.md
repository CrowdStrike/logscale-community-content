```
#repo=detections ExternalApiType=Event_IdpDetectionSummaryEvent
| rename([[TargetEndpointHostName, TargetEndpoint], [SourceEndpointHostName, SourceEndpoint], [TargetAccountName, TargetAccount], [SourceAccountName, SourceAccount]])
| format("[Detection](%s)", field=[FalconHostLink], as="Detect Link")
| table([@timestamp, SourceEndpoint, SourceAccount, TargetEndpoint, TargetAccount, DetectName, Severity, SeverityName, Tactic, Technique, Objective, "Detect Link"], limit=20000)
```

by Weighting...

```
#repo=detections ExternalApiType=Event_IdpDetectionSummaryEvent
| rename([[TargetEndpointHostName, TargetEndpoint], [SourceEndpointHostName, SourceEndpoint], [TargetAccountName, TargetAccount], [SourceAccountName, SourceAccount]])
| format("[FalconHostLink](%s)", field=[FalconHostLink], as="FalconHostLink")
| format(format="%s > %s", field=[Tactic, Technique], as=MITRE)
| groupBy([TargetAccount], function=([sum(Severity, as=Weight), count(DetectName, distinct=true, as=UniqueDetections), count(DetectName, as=TotalDetections), collect([MITRE, SourceEndpoint]), selectFromMax(field="@timestamp", include=[FalconHostLink])]))
| rename(field="FalconHostLink", as="Most Recent Detection")
| sort(Weight, order=desc, limit=200)
```