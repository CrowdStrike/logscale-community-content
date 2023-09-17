```
| ImageFileName=/Device\\HarddiskVolume\d+(?<FilePath>\\.+\\)(?<FileName>.+)$/i
```

Example of extracting file name and file path from ImageFileName:

```
#event_simpleName=ProcessRollup2 event_platform=Win
| ImageFileName=/Device\\HarddiskVolume\d+(?<FilePath>\\.+\\)(?<FileName>.+)$/i
| select([FileName, FilePath, ImageFileName])
```

[regex Documentation](https://library.humio.com/data-analysis/functions-regular-expression.html)
