Comment: In Legacy Event Search, `stats` is used to aggregate the output of a query. As an example:

```
| stats dc(aid) as uniqueEndpoints, count(aid) as totalExecutions, values(FileName) as fileNames by SHA256HashData
```

In LogScale, the `groupBy` function is used in concert with other aggregate functions. Example:

```
| groupBy([SHA256HashData], function=([count(aid, distinct=true, as=uniqueEndpoints), count(aid, as=totalExecutions), collect([FileName])]))
```

[[groupBy]]

