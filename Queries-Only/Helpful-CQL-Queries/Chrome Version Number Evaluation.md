```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<fileName>chrome\.exe)$/i
| groupBy([cid, aid, fileName, SHA256HashData])
| match(file="fdr_aidmaster.csv", field=aid, include=ComputerName, ignoreCase=true, strict=false)
| join({#event_simpleName=PeVersionInfo event_platform=Win | ImageFileName=/\\chrome\.exe/i | groupBy([SHA256HashData, FixedFileVersion, CompanyName], function=selectLast([ComputerName, FixedFileVersion]))}, include=[FixedFileVersion, CompanyName], field=[SHA256HashData])
| table([cid, aid, ComputerName, fileName, FixedFileVersion, CompanyName, _count, SHA256HashData])
| FixedFileVersion=/(?<majorVersion>\d+)\.(?<minorVersion>\d+)\.(?<buildNumber>\d+)\.(?<minorBuildNumber>\d+)$/i
| majorVersion < ?majorVersionLessThan AND minorVersion <= ?minorVersionLessThan
```

[[groupBy]] | [[match]]  | [[regex - extraction]] | [[regex]] 