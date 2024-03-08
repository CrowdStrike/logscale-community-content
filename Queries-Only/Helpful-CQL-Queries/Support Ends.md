```
#repo=sensor_metadata #data_source_name=aidmaster #data_source_group=aidmaster-api
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[ComputerName, Time, Version, ConfigIDBuild, AgentVersion])]))
| match(file="falcon/investigate/sensors_support_info.csv", field=ConfigIDBuild, column=BUILD, ignoreCase=true, strict=true)
| parseTimestamp("M/d/yy",field=SUPPORT_ENDS, as=SUPPORT_ENDS_EPOCH, timezone="UTC")
```

```
#repo=sensor_metadata #data_source_name=aidmaster #data_source_group=aidmaster-api
| groupBy([aid], function=([selectFromMax(field="@timestamp", include=[ComputerName, Time, Version, ConfigIDBuild, AgentVersion])]))
| match(file="falcon/investigate/sensors_support_info.csv", field=ConfigIDBuild, column=BUILD, ignoreCase=true, strict=true)
| parseTimestamp("M/d/yy",field=SUPPORT_ENDS, as=SUPPORT_ENDS_EPOCH, timezone="UTC")
| case{
    test(now()>SUPPORT_ENDS_EPOCH) | SUPPORTED:="NO";
    * | SUPPORTED:="YES";
}
| groupBy([PLATFORM, VERSION_FAMILY, SUPPORTED], function=([count(aid, as=Count), collect([RELEASE_DATE, SUPPORT_ENDS])]))
```