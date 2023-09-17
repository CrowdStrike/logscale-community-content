The `regex` function both works as a filter and can extract new fields using a regular expression. The regular expression can contain one or more named capturing groups. Fields with the names of the groups will be added to the events.

Inline

```
ImageFileName=/\\powershell\.exe/i
```

Function with Strict Matching

```
| regex("(sc|net1?)\s+(?<netFlag>\S+)\s+", field=CommandLine, strict=true)
```

Function with Non-Strict Matching

```
| regex("(sc|net1?)\s+(?<netFlag>\S+)\s+", field=CommandLine, strict=false)
```

The [`regex()`](https://library.humio.com/data-analysis/functions-regex.html "regex()") function provides similar functionality to the `/regex/` syntax, however, the [`regex()`](https://library.humio.com/data-analysis/functions-regex.html "regex()") function searches specific fields (and only [@rawstring](https://library.humio.com/data-analysis/searching-data-event-fields.html#searching-data-event-fields-metadata-rawstring) by default). In contrast, the `/regex/` syntax searches _all_ sent and parsed fields and [@rawstring](https://library.humio.com/data-analysis/searching-data-event-fields.html#searching-data-event-fields-metadata-rawstring).

If you specify a field with the `/regex/` syntax, the search is limited only to those field, for example:

```
| ImageFileName = /powershell/
```

Limits the search to only the specified field.

The difference in search scope between the two regex syntax operations introduces a significant performance difference between the two. Using [`regex()`](https://library.humio.com/data-analysis/functions-regex.html "regex()") searches only the specified field ([@rawstring](https://library.humio.com/data-analysis/searching-data-event-fields.html#searching-data-event-fields-metadata-rawstring) by default) and can be significantly more performant than the `/regex/` syntax depending on the number of fields in the dataset.

[regex Documentation](https://library.humio.com/data-analysis/functions-regular-expression.html)
