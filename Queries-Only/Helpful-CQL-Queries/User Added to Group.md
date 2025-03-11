```
#event_simpleName=UserAccountAddedToGroup
| parseInt(GroupRid, as="GroupRid", radix="16", endian="big")
| parseInt(UserRid, as="UserRid", radix="16", endian="big")
| UserSid:=format(format="%s-%s", field=[DomainSid, UserRid])
| groupBy([aid, UserSid], function=([selectFromMin(field="@timestamp", include=[RpcClientProcessId]), collect([ComputerName, DomainSid, UserRid])]))
| ContextTimeStamp:=ContextTimeStamp*1000
| ContextTimeStamp:=formatTime(format="%F %T", field="ContextTimeStamp")
| join(query={$falcon/investigate:usersid_username_win()}, field=[UserSid], include=UserName)
// Process Explorer - Uncomment the rootURL value that matches your cloud
| rootURL  := "https://falcon.crowdstrike.com/" /* US-1 */
//| rootURL  := "https://falcon.us-2.crowdstrike.com/" /* US-2 */
//| rootURL  := "https://falcon.laggar.gcw.crowdstrike.com/" /* Gov */
//| rootURL  := "https://falcon.eu-1.crowdstrike.com/"  /* EU */
| format("[Responsible Process](%sgraphs/process-explorer/tree?id=pid:%s:%s)", field=["rootURL", "aid", "RpcClientProcessId"], as="Process Explorer") 
| drop([rootURL, RpcClientProcessId])
```