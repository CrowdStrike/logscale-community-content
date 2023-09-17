Comments: In Legacy Event Search, the function `dedup` is used to remove events that match a specified set of fields. Example:

```
| dedup aid, ComputerName
```

In the above, any events with the same `aid` and `ComputerName` value will be discarded with the exception of the most recent by search order. 

While there is no `dedup` command in LogScale, `groupBy` can be used in a similar fashion:

```
#event_simpleName=ProcessRollup2
| groupBy([aid, ComputerName], function=([selectFromMax(field="@timestamp", include=[UserSid, UserName, ImageFileName, CommandLine])]))
```

In the above, LogScale will grab the most recent `ProcessRollup2` event for each `aid` and `ComputerName` combination and output the additional fields: `UserSid`, `UserName`, `ImageFileName`, and `CommandLine`.

As a note, `selectFromMin` can also be invoked as a function to get the oldest event in the search window.

```
#event_simpleName=ProcessRollup2
| groupBy([aid, ComputerName], function=([selectFromMMin(field="@timestamp", include=[UserSid, UserName, ImageFileName, CommandLine])]))
```

[[groupBy]]