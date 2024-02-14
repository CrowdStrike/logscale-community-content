```
(#repo=base_sensor #event_simpleName=UserAccountAddedToGroup)
| parseInt(GroupRid, as="GroupRid", radix="16", endian="big")
| parseInt(UserRid, as="UserRid", radix="16", endian="big")
| UserSid:=format(format="%s-%s", field=[DomainSid, UserRid])
| match(file="falcon/investigate/grouprid_wingroup.csv", field="GroupRid", column=GroupRid_dec, include=WinGroup)
| groupBy([aid, UserSid, ContextProcessId], function=([selectFromMin(field="@timestamp", include=[ContextTimeStamp]), collect([ WinGroup, GroupRid])]))
| ContextTimeStamp:=ContextTimeStamp*1000
| ContextTimeStamp:=formatTime(format="%F %T", field="ContextTimeStamp")
| join(query={#repo=sensor_metadata #data_source_name=usersid-ds}, field=[aid, UserSid], include=[UserName], mode=left)
| default(value="-", field=[UserName])
```