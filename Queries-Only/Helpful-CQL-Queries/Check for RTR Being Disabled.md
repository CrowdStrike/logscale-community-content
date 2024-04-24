```
#event_simpleName=SensorHeartbeat
| groupBy([aid], function=selectLast([@timestamp, ComputerName, SensorStateBitMap]), limit=max)
| bitfield:extractFlags(
field=SensorStateBitMap,
 output=[
   [2, RTR_Locally_Disabled]
])
| RTR_Locally_Disabled="true"
```