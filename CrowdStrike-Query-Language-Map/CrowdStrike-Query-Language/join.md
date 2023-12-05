Joins two LogScale searches. When joining two searches, you need to define the keys/fields that are used to match up results. This is done using the [`_field=name`](https://library.humio.com/data-analysis/functions-join.html#query-function-join-join-field "parameter to join():  Specifies which field in the event (log line) must match the given column value.  (click for more information)") or [`_field=[name,name,...`](https://library.humio.com/data-analysis/functions-join.html#query-function-join-join-field "parameter to join():  Specifies which field in the event (log line) must match the given column value.  (click for more information)") parameter.

```
| join({#event_simpleName=/^(UserIdentity|UserLogon)$/ | UserName!=/(\$$|^DWM-|LOCAL\sSERVICE|^UMFD-|^$)/}, field=UserSid, include=UserName, mode=left)
```

```
#event_simpleName=ProcessRollup2
| ImageFileName=/(?<FilePath>(\/|\\).+(\/|\\))(?<FileName>.+$)/
| FileName=~wildcard(?FileName, ignoreCase=true)
| select([aid, ComputerName, UserSid, UserName, FilePath, FileName, CommandLine])
| join({#event_simpleName=/^(UserIdentity|UserLogon)$/ | UserName!=/(\$$|^DWM-|LOCAL\sSERVICE|^UMFD-|^$)/}, field=UserSid, include=UserName, mode=left)
| UserName=~wildcard(?UserName, ignoreCase=true)
```

[join Documentation (1)](https://library.humio.com/data-analysis/functions-join.html) | [join Documenation (2)](https://library.humio.com/data-analysis/syntax-joins.html)

