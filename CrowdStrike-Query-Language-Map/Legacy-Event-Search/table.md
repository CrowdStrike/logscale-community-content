Comments: In Legacy Event Search, the `table` function is used to format columns in the desired order. Example:

```
| table aid, ComputerName, UserName, FileName, CommandLine
```

in LogScale:

```
| table([aid, ComputerName, UserName, FileName, CommandLine])
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/table|table]]

of note, the `select` function in LogScale performs the same operation and is more efficient. As such, using `select` is recommended:

```
| select([aid, ComputerName, UserName, FileName, CommandLine])
```

[[select]]


