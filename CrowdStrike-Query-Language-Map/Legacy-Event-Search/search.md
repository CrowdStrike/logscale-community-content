Comments: In Legacy Event Search, the `search` function is used when a subsequent search is required after the first line. Example:

```
event_platform=Win event_simpleName=ProcessRollup2
| search FileName="powershell.exe"
```

This function is not required in LogScale. Example translation:

```
event_platform=Win #event_simpleName=ProcessRollup2
| FileName="powershell.exe"
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/search|search]]


