In Legacy Event Search, the function `convert` is used to convert field values. Its most common use is with timestamps. Example:

```
| convert ctime(ProcessStartTime_decimal) as startTime
```

In LogScale,

```
#event_simpleName=ProcessRollup2 event_platform=Win
| startTime := ProcessStartTime*1000
| formatTime(format="%c", field=startTime, as=startTime)
| select([ProcessStartTime, startTime])
```

or

```
#event_simpleName=ProcessRollup2 event_platform=Win
| startTime := ProcessStartTime*1000
| formatTime(format="%Y %F.%L", field=startTime, as=startTime)
| select([ProcessStartTime, startTime])
```

Note: The function `formatTime` conforms to ISO-8601 and expects timestamps to be in millisecond-precision epoch time (e.g. `1687797202441`).

[[formatTime]]


