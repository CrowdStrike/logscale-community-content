Comments: In Legacy Event Search, the function `bucket` is used to aggregate output by a given time parameter. Example:

```
event_simpleName=OsVersionInfo
| bucket _time span=1d
| stats dc(aid) as endpointCount by _time
```

In LogScale:

```
#event_simpleName=OsVersionInfo
| bucket(1day, field=[#cid], function=(count(field=aid, distinct=true, as="endpointCount")))
| _bucket:=formatTime(format="%c", field="_bucket")
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/bucket|bucket]]


