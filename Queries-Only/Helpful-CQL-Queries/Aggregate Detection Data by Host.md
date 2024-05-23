```
ExternalApiType=Event_DetectionSummaryEvent
| format(format="%s > %s", field=[Tactic, Technique], as=MITRE)
| groupBy([AgentIdString], function=([count(DetectId, as=totalDetections), sum(Severity, as=severityWeight), min(@timestamp, as=firstDetect), max(@timestamp, as=lastDetect), collect([MITRE])]))
| formatTime(field=firstDetect, format="%Y-%m-%dT%H:%M:%S", as=firstDetect)
| formatTime(field=lastDetect, format="%Y-%m-%dT%H:%M:%S", as=lastDetect)
| sort(severityWeight, order=desc, limit=1000)
```
