Additional searches can be leveraged in LogScale by simply adding another pipe (`|`) to the query syntax. Example:

```
event_platform=Mac event_simpleName=UserLogon
| UserName="Andrew"
| UserSid!=S-1-5-18
| UserIsAdmin=1
```
