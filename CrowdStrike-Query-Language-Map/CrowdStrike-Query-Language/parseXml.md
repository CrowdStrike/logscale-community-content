The `parseXml` function will parse data as XML. Specify `field=@rawstring` to parse the `@rawstring` into XML. If the specified field does not exist, the event is skipped. If the specified field exists but contains non-XML data, the behaviors depends on the strict parameter.

```
#event_simpleName=ScheduledTaskRegistered
| parseXml(field=TaskXml)
| Task.Principals.Principal.UserId=*
| Task.Principals.Principal.UserId!=/^S-1-5-(18|20)$/
| select([aid, UserName, TaskName, TaskExecArguments, Task.Principals.Principal.RunLevel, Task.Principals.Principal.UserId, Task.Settings.Hidden, Task.Settings.Priority])
```

[parseXML Documentation](https://library.humio.com/data-analysis/functions-parsexml.html)
