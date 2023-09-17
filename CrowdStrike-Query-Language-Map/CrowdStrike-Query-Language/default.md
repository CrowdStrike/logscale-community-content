The `default`  function creates a field with the name of the parameter `field` setting its value to `value`. If the field already exists on an event the field keeps its existing value.

```
| default(value="Unknown", field=[GrandParentBaseFileName, ParentBaseFileName], replaceEmpty=true)
```

[default Documentation](https://library.humio.com/data-analysis/functions-default.html)
