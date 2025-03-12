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

Another Option:

```
// Get two events of interest
event_platform=Win #event_simpleName=/^(UserAccountAddedToGroup|ProcessRollup2)$/ 

// Begin data normalization
| case{
    // Rename fields in PR2 event
    #event_simpleName=ProcessRollup2 
        | rename(field="UserName", as="UserDoingAdding")
        | rename(field="FileName", as="FileDoingAdding")
        | rename(field="CommandLine", as="AssociatedCommandLine");

    // Rename and prase fields in UserAccount event
    #event_simpleName= UserAccountAddedToGroup
        | TargetProcessId:=RpcClientProcessId
        | parseInt(GroupRid, as="GroupRid", radix="16", endian="big")
        | parseInt(UserRid, as="UserRid", radix="16", endian="big")
        | UserSid:=format(format="%s-%s", field=[DomainSid, UserRid]);
}

// User selfJoinFilter() to narrow dataset
| selfJoinFilter(field=[aid, TargetProcessId], where=[{#event_simpleName=ProcessRollup2},{#event_simpleName=UserAccountAddedToGroup}])

// Aggregate results
| groupBy([aid, TargetProcessId, ComputerName], function=([{#event_simpleName="UserAccountAddedToGroup" | collect([UserSid])}, collect([UserDoingAdding, UserAddedToGroup, FileDoingAdding, AssociatedCommandLine]), collect([GroupRid], separator=", ")]))

// Match the UserSid of the account that was added to a group with its corresponding UserName
| join(query={$falcon/investigate:usersid_username_win() | rename(field="UserName", as="UserAddedToGroup")}, field=[UserSid], include=UserAddedToGroup, mode=left, start=7d)

// Drop UserSid
| drop([UserSid])

// Make sure there are not FPs from selfJoinFilter()
| UserAddedToGroup=* UserDoingAdding=*
```