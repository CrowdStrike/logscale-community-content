https://attack.mitre.org/techniques/T1217/

All

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ /bookmarks/i
| /(firefox|chrome|edge|iexplore)/i
```