Comments: In Legacy Event Search, the `rename` function is used to change the name of a specified field. Example:

```
| rename aid as "Agent ID", ComputerName as "Endpoint", UserSid_readable as "User SID"
```

A similar function exists in LogScale. Each `rename` request requires its own line. Example:

```
| rename(field="aid", as="Agent ID")
| rename(field="ComputerName", as="Endpoint")
| rename(field="UserSid", as="User SID")
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/rename|rename]]


