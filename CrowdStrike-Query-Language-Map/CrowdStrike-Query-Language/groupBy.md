The `groupBy()` query function is used to group together events by one or more specified fields. This is similar to the `GROUP BY` method in SQL databases. Further, it can be used to execute aggregate functions on each group. The results are returned in the `_field` parameter for each aggregate function. For example, the `_count` field if the [`count()`](https://library.humio.com/data-analysis/functions-count.html "Counts given events.      (click for more information)") function is used.

```
| groupBy([aid, UserSid], function=([count(aid, as=exeuctionCount), collect([CommandLine])]), limit=max)
```

[groupBy Documentation](https://library.humio.com/data-analysis/functions-groupby.html)
