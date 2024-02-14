The `default`  function creates a field with the name of the parameter `field` setting its value to `value`. If the field already exists on an event the field keeps its existing value.

```
| default(value="Unknown", field=[GrandParentBaseFileName, ParentBaseFileName], replaceEmpty=true)
```

Of note, while `replaceEmpty=true` is optional, it is necessary to populate files that are listed as `<empty_string>`.


[default Documentation](https://library.humio.com/data-analysis/functions-default.html)
