```
id := hash([fields_to_count], limit=1000000) // Uses hash collision to increase cardinality the limit here needs to max the limit in the first groupby
| groupBy([id], limit=max, function={ groupBy([fields_to_count], function=[], limit=max)| count() }) // Count the sub groups
| sum("_count") // Sum all the counts
```

[Reference](https://www.reddit.com/r/crowdstrike/comments/1q5w238/help_needed_logscale_query_to_count_unique_pairs/)
