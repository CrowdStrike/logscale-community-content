https://attack.mitre.org/techniques/T1057/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\tasklist\.exe/) OR (/(Get-Process|CreateToolhelp32Snapshot)/i))
```

Linux/macOS

```
#event_simpleName=ProcessRollup2 event_platform=Lin ImageFileName=/\/ps/
```