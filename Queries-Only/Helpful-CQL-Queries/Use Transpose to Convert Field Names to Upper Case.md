```
| createEvents(["color=blue", "shape=round", "size=large"])
| kvParse()
| transpose(limit=1000)
| column := upper(column)
| transpose(header=column,limit=1000)
| drop(column)
```