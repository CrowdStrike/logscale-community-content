The function `kvParse` is used to parse key-values of the form:

- `key=value`
- `key="value"`
- `key='value'`
- `key = value`

Both key and value can be either quoted using `"` or `'`, or unquoted.

```
createEvents(["Shape=Square, Color=Red", "Shape=Circle, Color=Blue", "Shape=Triangle, Color=Green"])
| kvParse()
```

[kvParse Documentation](https://library.humio.com/data-analysis/functions-kvparse.html)
