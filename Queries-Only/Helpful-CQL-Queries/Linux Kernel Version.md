```
#event_simpleName=OsVersionInfo event_platform=Lin
| groupby(aid, function=selectLast([OSVersionString]))
| OSVersionString=/Linux\s+\S+\s(?<kernelVersion>\S+)\s.*/
| top("kernelVersion", limit=100)

```