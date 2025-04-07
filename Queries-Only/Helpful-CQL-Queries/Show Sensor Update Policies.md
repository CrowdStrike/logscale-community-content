```
defineTable(
    query={
        #repo="sensor_metadata" #data_source_name="policyinfo" #data_source_group="sensor-update"
        | groupBy(id, function=selectFromMax(field="@timestamp", include=[release_id]))
        | rename(field="id", as="sensor_update_policy_id")
    }
    , include=[sensor_update_policy_id, release_id]
    , name="policy_to_release"
    , start=1h // policyinfo is currently updated once an hour
)
| defineTable(query={
    createEvents([
        "release_id=tagged|1 release.type=N-1",
        "release_id=tagged|2 release.type=N-2",
        "release_id=tagged|3 release.type=N-1",
        "release_id=tagged|4 release.type=N-2",
        "release_id=tagged|5 release.type=N-1",
        "release_id=tagged|6 release.type=N-2",
        "release_id=tagged|11 release.type=\"Auto Latest\"",
        "release_id=tagged|12 release.type=\"Auto Latest\"",
        "release_id=tagged|13 release.type=\"Auto Latest\"",
        "release_id=tagged|16 release.type=\"Auto EA\"",
        "release_id=tagged|17 release.type=\"Auto EA\"",
        "release_id=tagged|18 release.type=\"Auto EA\""
    ])
    | kvParse()
}, include=[release_id, release.type], name="release_type_lookup")
| defineTable(
    query={
        #repo="sensor_metadata" #data_source_name="aid-policy"
        | groupBy(aid, limit=max, function=selectFromMax(field="@timestamp", include=[sensor_update_policy_id]))
    }
    , include=[aid, sensor_update_policy_id]
    , name="aid_to_policy"
    , start=1d //aid-policy is currently updated once per day
)
| readFile("aid_master_main.csv")
| in(field="ProductType", values=[1,2,3])
| match(file="aid_to_policy", field=aid, include=sensor_update_policy_id)
| match(file="policy_to_release", field=sensor_update_policy_id, include=release_id, strict=false)
| match(file="release_type_lookup", field=[release_id], include=release.type, strict=false)
| groupBy([cid, aid, ComputerName, event_platform, Version, FirstSeen, ProductType, MAC, sensor_update_policy_id, release.type, MachineDomain, OU, SiteName, SystemManufacturer, SystemProductName], function=[], limit=max)
| default(value="-", field=[ProductType, MAC, sensor_update_policy_id, MachineDomain, OU, SiteName, SystemManufacturer, SystemProductName], replaceEmpty=true)
| default(value="Auto-Update Disabled", field=[release.type])
```