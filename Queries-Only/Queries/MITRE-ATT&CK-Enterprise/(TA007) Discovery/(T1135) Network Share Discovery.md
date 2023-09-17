https://attack.mitre.org/techniques/T1135/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\net1?\.exe/i CommandLine=/\s+(view|share)\s+/i) OR (ImageFileName=/\\netview\.exe/i) OR (/NetShareEnum/))
```

macOS

```
#event_simpleName=ProcessRollup2 event_platform=Mac ImageFileName=/\/sharing$/i CommandLine=/\-l/i
```