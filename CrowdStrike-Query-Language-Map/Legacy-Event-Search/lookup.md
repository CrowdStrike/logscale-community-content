In Legacy Event Search, the `lookup` function is used to invoke field value lookups. Example:

```
| lookup local=true aid_master aid OUTPUT ComputerName, Version, AgentVersion
```

in LogScale:

```
 match(file="fdr_aidmaster.csv", field=aid, include=[ComputerName, Version, AgentVersion], ignoreCase=true, strict=false)
```

[[match (lookup)]]

