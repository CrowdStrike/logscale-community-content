
https://attack.mitre.org/techniques/T1010/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win /(mainWindowTitle|Get-Process|GetForegroundWindow|mainWindowTitle)/i
```