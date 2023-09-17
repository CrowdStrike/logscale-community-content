```
#event_simpleName=UserLogon UserSid=/S-1-5-21-/
| top([UserName], limit=100)
```

[top Documentation](https://library.humio.com/data-analysis/functions-top.html)