Comments: In Legacy Event Search, the `sort` function is used to organize the ordering of columns. Example:

```
| sort +ComputerName
```

or

```
| sort -ComputerName
```

In LogScale:

```
| sort(ComputerName, order=asc, limit=200)
```

or

```
| sort(ComputerName, order=desc, limit=200)
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/sort|sort]]


