The `bucket` function divides the search time interval into buckets. Each event is put into a bucket based on its timestamp value.

Events are grouped by their bucket, generating the field `_bucket`. The value of `_bucket` is the corresponding bucket's start time in milliseconds (UTC time).

The `bucket()` function takes all the same parameters as `groupBy()`.

```
| bucket(1day, field=[RFMState], function=(count(field=aid, as="endpointCount")))
```

Example in counting RFM Linux systems by day:

```
#event_simpleName=OsVersionInfo RFMState=*
| day := formatTime("%Y-%m-%d", field=@timestamp, locale=en_US, timezone=Z)
| groupBy([aid, day], function=(selectLast([RFMState, @timestamp])), limit=max)
| RFMState match {
	1 => RFMState := "RFM" ;
	0 => RFMState := "OK" ;
	}
| bucket(1day, field=[RFMState], function=(count(field=aid, as="endpointCount")))
| _bucket := formatTime("%Y-%m-%d", field=_bucket, locale=en_US, timezone=Z)
```

[bucket Documentation](https://library.humio.com/data-analysis/functions-bucket.html)
