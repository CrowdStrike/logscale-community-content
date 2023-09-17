Comments: In Legacy Event Search, the function `makemv` is used to convert a field into a multi-value field. Example:

```
event_simpleName=DnsRequest
| makemv IP4Records delim=";" 
| stats values(IP4Records) as IP4Records by DomainName
```

In LogScale:

```
#event_simpleName=DnsRequest
| splitString(IP4Records, by=";", as=IP4RecordsSplit)
| concatArray(IP4RecordsSplit, as=IP4RecordsMV, separator="\n")
| groupBy([DomainName], function=([collect([IP4RecordsMV]), count(IP4RecordsMV, distinct=true)]))
```

The function `splitString` will create an array of values. The function `concatArray` will then collapse that array into a single, multi-value field with a specified delimiter. 

[[splitString]] | [[concatArray]]
