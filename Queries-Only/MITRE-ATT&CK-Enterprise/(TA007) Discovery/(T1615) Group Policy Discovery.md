https://attack.mitre.org/techniques/T1615/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\gpresult\.exe/i) OR /(Get-DomainGPO|Get-DomainGPOLocalGroup|GPOLocalGroup)/i)
```
