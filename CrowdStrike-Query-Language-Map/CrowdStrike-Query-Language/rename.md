The `rename` function renames a field.

```
| rename(aid, as="Falcon Agent ID")
```

the `rename` function can also accept arrays:

```
| rename([[ComputerName, Endpoint], [UserName, User]])
```

[rename Documentation](https://library.humio.com/data-analysis/functions-rename.html)
