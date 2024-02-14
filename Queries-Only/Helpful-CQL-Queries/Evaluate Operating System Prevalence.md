```
#event_simpleName=OsVersionInfo event_platform=Win

| groupby(aid, function=selectLast([ProductName]))
| groupBy([ProductName], function=stats([count(aid, as="endpointCount")]))

```