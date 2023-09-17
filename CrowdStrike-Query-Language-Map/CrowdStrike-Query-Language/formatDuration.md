The `formatDuration` function will convert a duration into a human readable string. The `from` parameter can be set to your duration's magnitude.

|   |   |   |
|---|---|---|
|**Valid Values**|`d`|Days|
||`h`|Hours|
||`m`|Minutes|
||`ms`|Milliseconds|
||`ns`|Nanoseconds|
||`s`|Seconds|
||`us`|Microseconds|

```
| formatDuration(timeDelta, from=ms, precision=4, as=timeDelta)
```

[formatDuration Documentation](https://library.humio.com/data-analysis/functions-formatduration.html)
