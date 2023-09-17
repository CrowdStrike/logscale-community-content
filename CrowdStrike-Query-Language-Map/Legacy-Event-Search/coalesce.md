Comments: In Legacy Event Search, the function `coalesce` is used to evaluate one or more values and return the first value that is not null. Example:

```
| eval falconPID=coalesce(TargetProcessId_decimal, ContextProcessId_decimal)
```

In LogScale, the same outcome can be reached using `concat` or the assignment operator. Examples:

```
| falconPID:=concat([TargetProcessId, ContextProcessId])
```

or

```
| falconPID:=TargetProcessId
| falconPID:=ContextProcessId
```

[[concat]] | [[assignment operator]]
