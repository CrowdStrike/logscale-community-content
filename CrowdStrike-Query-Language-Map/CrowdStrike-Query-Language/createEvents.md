The `createEvents()` query function generates temporary events as part of the query and is ideal for generating sample data for testing or troubleshooting. It is regarded as an aggregator function and, therefore, discards all incoming events and outputs the generated ones. The events are generated with no extracted fields but `createEvents()` can be combined with one of the many parsers. For example, given raw strings in the format of key-value pairs, the pairs can be parsed to fields using the `kvParse()` function.

```
createEvents(["Shape=Square, Color=Red", "Shape=Circle, Color=Blue", "Shape=Triangle, Color=Green"])
```

With field parsing:

```
createEvents(["Shape=Square, Color=Red", "Shape=Circle, Color=Blue", "Shape=Triangle, Color=Green"])
| kvParse()
```

[createEvents Documentation](https://library.humio.com/data-analysis/functions-createevents.html)
