https://attack.mitre.org/techniques/T1580/

All

```
(#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(DescribeInstances|ListBuckets|HeadBucket|GetPublicAccessBlock|DescribeDBInstances)/i) OR (#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(gcloud\s+compute\s+instances\s+list)/i) OR (#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /(az\s+vm\s+list)/i)
```