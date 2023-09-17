The `concat` query function is used to format a string using `printf` style. The formatted string is put in a new field. The input parameters or fields can be one field or an array of fields. See also: [[concat]].

```
| format(format="%s > %s > %s { %s }", field=[GrandParentBaseFileName, ParentBaseFileName, fileName, CommandLine], as="processLineage")
```

[format Documentation](https://library.humio.com/data-analysis/functions-format.html#query-function-format-format-format)
