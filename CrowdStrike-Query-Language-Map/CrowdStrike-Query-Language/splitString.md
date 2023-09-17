```
| splitString(field=CommandLine, by=",", as=CommandLine)
| split(CommandLine)
```

[splitString Documentation](https://library.humio.com/data-analysis/functions-splitstring.html)
[split Documentation](https://library.humio.com/data-analysis/functions-split.html)

Additional option to split a multi-value, comma separated field using regex:

```
| CommandLine=/(?<CommandLine>[^,]+)/g
| groupBy([CommandLine])
```

[regex Field Extraction Documentation](https://library.humio.com/data-analysis/syntax-fields.html#syntax-fields-extracting)
