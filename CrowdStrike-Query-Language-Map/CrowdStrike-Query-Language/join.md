Joins two LogScale searches. When joining two searches, you need to define the keys/fields that are used to match up results. This is done using the [`_field=name`](https://library.humio.com/data-analysis/functions-join.html#query-function-join-join-field "parameter to join():  Specifies which field in the event (log line) must match the given column value.  (click for more information)") or [`_field=[name,name,...`](https://library.humio.com/data-analysis/functions-join.html#query-function-join-join-field "parameter to join():  Specifies which field in the event (log line) must match the given column value.  (click for more information)") parameter.

```
#event_simpleName=ProcessRollup2 event_platform=Win ImageFileName=/\\(?<fileName>chrome\.exe)$/i
| groupBy([cid, aid, fileName, SHA256HashData])
| join({#event_simpleName=PeVersionInfo event_platform=Win | ImageFileName=/\\chrome\.exe/i | groupBy([SHA256HashData, FixedFileVersion, CompanyName], function=selectLast([FixedFileVersion]))}, include=[FixedFileVersion, CompanyName], field=[SHA256HashData])
| table([cid, aid, fileName, FixedFileVersion, CompanyName, _count, SHA256HashData])
```

[join Documentation (1)](https://library.humio.com/data-analysis/functions-join.html) | [join Documenation (2)](https://library.humio.com/data-analysis/syntax-joins.html)

