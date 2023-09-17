Comments: In Legacy Event Search, the function `mvsplit` is used to split multi-value fields that leverage a common delimiter. Example:

```
event_simpleName=DnsRequest IP4Records=*
| eval ipv4Records=split(IP4Records, ";") 
| stats values(ipv4Records) as ipv4Records by DomainName 
```

In LogScale:

```
#event_simpleName=DnsRequest IP4Records=*
| splitString(field=IP4Records, by=";", as=ipv4Records)
| split(ipv4Records)
| groupBy([DomainName], function=collect([ipv4Records]))
```

[[splitString]]
