The `concatArray` function concatenates the values of all fields with the same name and an array suffix into a value in a new field. Such array fields typically come as output from either `parseJson()` or `splitString()`.

All array fields starting with index from and ending with index to are selected. If an index is missing, the concatenation stops with the previous index, thus if only index `0`, `1` and `3` are present, only index `0` and `1` are concatenated. If the first index is missing, no field is added to the event.

```
#event_simpleName=DnsRequest
| splitString(IP4Records, by=";", as=IP4RecordsSplit)
| concatArray(IP4RecordsSplit, as=IP4RecordsMV, separator="\n")
| groupBy([DomainName], function=([collect([IP4RecordsMV]), count(IP4RecordsMV, distinct=true)]))
| test(_count>0)
```

[concatArray Documentation](https://library.humio.com/data-analysis/functions-concatarray.html)
