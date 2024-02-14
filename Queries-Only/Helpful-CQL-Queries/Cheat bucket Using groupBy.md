```
#event_simpleName=OsVersionInfo  RFMState=*
| day := formatTime("%Y-%m-%d", field=@timestamp, locale=en_US, timezone=Z)
| groupBy([aid, day], function=(selectLast([RFMState, @timestamp])), limit=max)
| RFMState match {
    1 => RFMState := "True" ;
    0 => RFMState := "False" ;
}
| groupBy([day, RFMState], function=count(aid))
```

[[groupBy]] | [[match]] 