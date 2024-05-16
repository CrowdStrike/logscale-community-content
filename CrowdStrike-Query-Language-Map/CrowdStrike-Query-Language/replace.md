The `replace` function replaces each substring of the specified fields value that matches the given regular expression with the given replacement.

```
| replace(regex=^apples$, with=oranges)
```

```
| ip =~replace(".", with="")
```

[replace Documentation](https://library.humio.com/data-analysis/functions-replace.html)
