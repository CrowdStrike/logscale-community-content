Comments: In Legacy Event Search, the `rare` function is used to detect the least common fields or in an event. Example:

```
event_simpleName=UserLogon
rare UserName
```

In LogScale, the `groupBy` function can be used to acheive the same outcome:

```
#event_simpleName=UserLogon
| groupBy([UserName], function=([count(UserName)]))
| sort(_count, order=asc, limit=10)
```

[[groupBy]] | [[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/sort|sort]]

