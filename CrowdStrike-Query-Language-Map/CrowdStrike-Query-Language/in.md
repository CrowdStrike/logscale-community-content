The `in` function may be used to select events in which the given field contains particular values. For instance, you might want to monitor events in which log messages contain `error`, `warning`, or other similar words in log entries, or numeric values in other fields.

```
| in(LogonDomain, values=["acme.com","beta.com"])
```

```
| in(LogonType, values=[2,10])
```

[in Documentation](https://library.humio.com/data-analysis/functions-in.html)
