```
#event_simpleName=DetectionExcluded ExclusionSource=6
| PatternId =~ match(file="falcon/investigate/detect_patterns.csv", column=PatternId, strict=false)
| case {
    ExclusionType=1 | ExclusionType_Readable:="IOA" | Detail:=CommandLine;
    ExclusionType=2 | ExclusionType_Readable:="IOC" | Detail:=TargetSHA256HashData;
    ExclusionType=4 | ExclusionType_Readable:="Certificate" | Detail:=TargetSHA256HashData;
    *;
}
| groupBy([Tactic, Technique, ExclusionType_Readable, description], function=([count(aid, as=TotalDetections), collect([Detail, DetectName])]))
| table([TotalDetections, ExclusionType_Readable, DetectName, Tactic, Technique, Detail], limit=20000, sortby=TotalDetections)
```