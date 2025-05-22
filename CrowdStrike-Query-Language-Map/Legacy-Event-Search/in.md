Comments: In Legacy Event Search, the modifier `IN` can be used to include or exclude multiple field values. Example:

```
event_simpleName=ProcessRollup2 FileName IN (cmd.exe, powershell.exe)
```

In LogScale, the `in` function can be used:

```
#event_simpleName=ProcessRollup2
| in(field="FileName", values=[cmd.exe, powershell.exe])
```

Note that in LogScale, regex is available nearly anywhere and can also be used:

```
#event_simpleName=ProcessRollup2 FileName=/^(powershell|cmd)\.exe$/i
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/in|in]] 

