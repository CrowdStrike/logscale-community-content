Comments: In Legacy Event Search, the function `top` is used to aggregate a fixed number of results based on frequency. Example:

```
event_simpleName=UserLogon "S-1-5-21-"
| top UserName, event_platform
```

In LogScale:

```
#event_simpleName=UserLogon UserSid=/S-1-5-21-/
| top([UserName, event_platform])
```

to include percentage of total:

```
#event_simpleName=UserLogon UserSid=/S-1-5-21-/
| top([UserName, event_platform], percent=true)
```

[[CrowdStrike-Query-Language-Map/CrowdStrike-Query-Language/top|top]]


