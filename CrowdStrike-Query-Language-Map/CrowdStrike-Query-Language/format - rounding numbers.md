The following takes a field that contains and integer and rounds it to two decimal places. The value `2f` can be changed to the number of decimal places desired. If no decimal places are required, consider using the [[round]] function:

```
| FileSizeMB:=(Size/1024/1024)
| format("%,.2f",field=["FileSizeMB"], as="FileSize")
```

Rounding with a unit indicator:

```
| FileSizeMB:=(Size/1024/1024)
| format("%,.2f MB",field=["FileSizeMB"], as="FileSize")
```

[format Documentation](https://library.humio.com/data-analysis/functions-format.html#functions-format-examples)
