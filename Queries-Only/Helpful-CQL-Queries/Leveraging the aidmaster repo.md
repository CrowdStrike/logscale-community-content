```
#repo=sensor_metadata #data_source_name=aidmaster
| groupBy([cid, aid], function=([selectFromMax(field="@timestamp", include=[AgentLoadFlags, AgentLocalTime, AgentTimeOffset, AgentVersion, BiosManufacturer, BiosVersion, ChassisType, City, ComputerName, ConfigBuild, ConfigIDBuild, Continent, Country, FalconGroupingTags, FirstSeen, HostHiddenStatus, MachineDomain, OU, PointerSize, ProductType, SensorGroupingTags, ServicePackMajor, SiteName, SystemManufacturer, SystemProductName, @timezone, Timezone, Version, aid, aip, cid, event_platform])]))
| lastSeen:=@timestamp
| formatTime(format="%F %T", as="lastSeen", field=lastSeen)
| timeDelta:=now()-@timestamp
| timeDeltaDays:=timeDelta/1000/60/60/24
| round(timeDeltaDays)
  
// Edit this line to set your "days since last seen" treshold
//| timeDeltaDays<4
  
| ipLocation(aip)
| drop([aip.lat, aip.lon, timeDelta, @timestamp])
```