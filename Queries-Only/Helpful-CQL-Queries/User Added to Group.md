```
(#repo=base_sensor #event_simpleName=UserAccountAddedToGroup)
| parseInt(GroupRid, as="GroupRid", radix="16", endian="big")
| parseInt(UserRid, as="UserRid", radix="16", endian="big")
| UserSid:=format(format="%s-%s", field=[DomainSid, UserRid])
| match(file="falcon/investigate/grouprid_wingroup.csv", field="GroupRid", column=GroupRid_dec, include=WinGroup)
| Groups:=format(format="%s (%s)", field=[WinGroup, GroupRid])
| groupBy([aid, UserSid], function=([selectFromMin(field="@timestamp", include=[RpcClientProcessId]), collect([ComputerName, Groups])]))
| ContextTimeStamp:=ContextTimeStamp*1000
| ContextTimeStamp:=formatTime(format="%F %T", field="ContextTimeStamp")
| join(query={#repo=sensor_metadata #data_source_name=userinfo-ds}, field=[UserSid], include=[UserName], mode=left, start=7d)
| default(value="-", field=[UserName])
// Process Explorer - Uncomment the rootURL value that matches your cloud
| rootURL  := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Responsible Process](%sgraphs/process-explorer/tree?id=pid:%s:%s)", field=["rootURL", "aid", "RpcClientProcessId"], as="Process Explorer") 
| drop([rootURL, RpcClientProcessId])
```