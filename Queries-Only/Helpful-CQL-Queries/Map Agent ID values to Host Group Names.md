```
#repo=sensor_metadata
#data_source_name=aid-policy
| parseJson(field=groups, prefix=groups_arr)
| concatArray(groups_arr, separator=",", as=groups_arr)
| splitString(field=groups_arr, by=",", as=group_id)
| split(group_id)
| replace("[\[\]']+", with="", field=groups)
| join({
  $falcon/investigate:group_info()
}, field=group_id, include=name, mode=left, start=5d)
| group_name := rename(name)
| default(field=[group_name],value="Default",replaceEmpty="true")
| groupBy([aid, group_id, group_name])
```