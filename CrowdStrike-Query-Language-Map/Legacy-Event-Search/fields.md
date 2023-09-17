Comment: In Legacy Event Search, the `fields` function can narrow the outputs of a given aggregation or search. Example:

```
event_simpleName=ProcessRollup2
| fields aid, ImageFileName, CommandLine
```

In LogScale, `select` can be used to achieve the same objective:

```
#event_simpleName=ProcessRollup2
| select([aid, ImageFileName, CommandLine])
```

[[select]]

Alternatively, the function `drop` can be used to omit specific fields pre or post aggregation:

```
#event_simpleName=ProcessRollup2 
| groupBy([ImageFileName, CommandLine])
| drop([_count])
```

[[drop]]
