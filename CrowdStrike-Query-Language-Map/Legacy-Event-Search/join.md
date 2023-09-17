Comments: In Legacy Event Search, the `join` function is used to join two datasets via a key field(s). Example:

```
event_simpleName=ProcessRollup2 event_platform=Win FileName=chrome.exe
| join aid, SHA256HashData 
    [search event_simpleName=PeVersionInfo event_platform=Win FileName=chrome.exe]
| stats latest(ComputerName) as ComputerName, latest(FileVersion) as FileVersion by cid, aid, SHA256HashData, FixedFileVersion, CompanyName
| table cid, aid, ComputerName, fileName, FixedFileVersion, CompanyName, SHA256HashData
```

In LogScale:

```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<fileName>chrome\.exe)$/i
| groupBy([cid, aid, fileName, SHA256HashData])
| join({#event_simpleName=PeVersionInfo event_platform=Win | ImageFileName=/\\chrome\.exe/i | groupBy([SHA256HashData, FixedFileVersion, CompanyName], function=selectLast([FixedFileVersion]))}, include=[FixedFileVersion, CompanyName], field=[SHA256HashData])
| table([cid, aid, fileName, FixedFileVersion, CompanyName, SHA256HashData])
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/join|join]]


