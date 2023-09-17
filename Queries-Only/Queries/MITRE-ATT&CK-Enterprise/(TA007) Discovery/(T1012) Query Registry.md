https://attack.mitre.org/techniques/T1012/

Windows

```
#event_simpleName=/^(ProcessRollup2|CommandHistory|ScriptControl)/ event_platform=Win ((ImageFileName=/\\reg\.exe/) OR (/(RegOpenKeyEx|RegOpenUserClassesRoot|HKEY_CLASSES_ROOT|HKCR)/i))
```

```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\reg\.exe/
| ImageFileName=/^//.+//(?<FileName>reg\.exe)/
| FileName:=lower("FileName") 
| ParentBaseFileName:=lower("ParentBaseFileName")
| groupBy([ParentBaseFileName, FileName], function=([count(aid, as=executionCount), count(aid, distinct=true, as=totalEndpoints)]))
| sort(executionCount, order=asc)
```
